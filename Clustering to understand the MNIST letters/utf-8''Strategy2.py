
  kernel = [[0,-1,0],[-1,5,-1],[0,-1,0]]
  e = 0
  f = 0
  g = 2
  h = 2
  t = []
  
  print(kernel)
  while g > 0:
    while h > 0:
      t = kernel[e][f]
      kernel[e][f] = kernel[g][h]
      kernel[g][h] = kernel[e][f]
      h -+1
      f +=1
  g -=1
  e +=1
  print (kernel)