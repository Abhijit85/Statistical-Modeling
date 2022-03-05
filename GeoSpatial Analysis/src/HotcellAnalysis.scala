package cse512

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.functions._

object HotcellAnalysis {
  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

  def runHotcellAnalysis(spark: SparkSession, pointPath: String): DataFrame = {
    // Load the original data from a data source
    var pickupInfo = spark.read.format("com.databricks.spark.csv").option("delimiter", ";").option("header", "false").load(pointPath);
    pickupInfo.createOrReplaceTempView("nyctaxitrips")
    pickupInfo.show()

    // Assign cell coordinates based on pickup points
    spark.udf.register("CalculateX", (pickupPoint: String) => ((
      HotcellUtils.CalculateCoordinate(pickupPoint, 0)
      )))
    spark.udf.register("CalculateY", (pickupPoint: String) => ((
      HotcellUtils.CalculateCoordinate(pickupPoint, 1)
      )))
    spark.udf.register("CalculateZ", (pickupTime: String) => ((
      HotcellUtils.CalculateCoordinate(pickupTime, 2)
      )))
    pickupInfo = spark.sql("select CalculateX(nyctaxitrips._c5),CalculateY(nyctaxitrips._c5), CalculateZ(nyctaxitrips._c1) from nyctaxitrips")
    var newCoordinateName = Seq("x", "y", "z")
    pickupInfo = pickupInfo.toDF(newCoordinateName: _*)
    pickupInfo.show()

    // Define the min and max of x, y, z
    val minX = -74.50 / HotcellUtils.coordinateStep
    val maxX = -73.70 / HotcellUtils.coordinateStep
    val minY = 40.50 / HotcellUtils.coordinateStep
    val maxY = 40.90 / HotcellUtils.coordinateStep
    val minZ = 1
    val maxZ = 31
    val numCells = (maxX - minX + 1) * (maxY - minY + 1) * (maxZ - minZ + 1)

    // YOU NEED TO CHANGE THIS PART
    val cellDf = pickupInfo.groupBy("x", "y", "z").agg(count("*").alias("attribute"))
    cellDf.createOrReplaceTempView("cells")
    val sigmaA = cellDf.agg(sum("attribute")).first().getLong(0).toDouble
    val sigmaA2 = cellDf.agg(sum(pow("attribute", 2))).first().getDouble(0)
    val mean = sigmaA / numCells
    val std = math.sqrt(sigmaA2 / numCells - mean * mean)
    spark.udf.register("calculateG", (sigmaWA: Double, sigmaW: Double) =>
      HotcellUtils.calculateG(sigmaWA, sigmaW, mean, std, numCells)
    )
    spark.udf.register("calculateSigmaW", (x: Int, y: Int, z: Int) =>
      HotcellUtils.calculateSigmaW(x, y, z, minX.toInt, minY.toInt, minZ.toInt, maxX.toInt, maxY.toInt, maxZ.toInt)
    )
    spark.udf.register("isNeighbor", HotcellUtils.isNeighbor _)

    //cellDf.show()
    val nbrDf = spark.sql(
      "SELECT cells.x,cells.y,cells.z,cells.attribute,nbr.attribute AS nbrAttribute FROM cells"
        + " JOIN cells nbr ON isNeighbor(cells.x, cells.y, cells.z, nbr.x, nbr.y, nbr.z)")
    nbrDf.createOrReplaceTempView("neighbor")
    //nbrDf.show()
    val cellStatDf = spark.sql(
      "SELECT x,y,z,sum(nbrAttribute) AS sigmaWA,calculateSigmaW(x,y,z) AS sigmaW FROM neighbor GROUP BY x,y,z"
    )
    cellStatDf.createOrReplaceTempView("cellStat")
    //cellStatDf.show()

    val gDf = spark.sql("SELECT x,y,z FROM cellStat ORDER BY calculateG(sigmaWA, sigmaW) desc")
    //gDf.show()
    return gDf

  }
}
