import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Getting user input for city (chicago, new york city, washington).
    check_flag = True
    while check_flag:
        city = input('Please choose a city from chicago/new york city/washington: ')
        city = city.lower()
        if city not in ('chicago','new york city','washington'):
                print('Kindly choose from the list of choices provided')
        else:
            break

    # Getting user input for month (all, january, february, ... , june)
    while check_flag:
        month = input('Please choose a month from january, february, march, april, may, june OR type in all to consider all the months: ')
        month = month.lower()
        if month not in ('january','february','march', 'april', 'may', 'june','all'):
            print('Kindly choose from the list of choices provided')
        else:
            break



    # Getting user input for day of week (all, monday, tuesday, ... sunday)
    while check_flag:
        day = input('Please choose a  day of week from  monday, tuesday, wednesday, thusrday, friday, saturday, sunday OR type in all to consider all the days: ')
        day = day.lower()
        if day not in ('monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday','all'):
            print('Kindly choose from the list of choices provided')
        else:
            break



    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filtering by month if applicable
    if month != 'all':

        # Using the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filtering by month to create the new dataframe

        df = df[df['month'] == month]

        # Filtering by day of week if applicable
        if day != 'all':
            df = df[df['day_of_week'] == day.title()]
		# Filtering by day of week to create the new dataframe



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

	# Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Displaying the most common month

    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    # Display the most common day of week

    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most common day of week:', popular_day)

    # Displaying the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['Stations'] = df['Start Station'].str.cat(df['End Station'],sep=",")

    # Displaying most commonly used start station
    print('Most commonly used start station:', df['Start Station'].mode()[0])

    # Displaying most commonly used end station
    print('Most commonly used end station:', df['End Station'].mode()[0])

    # Displaying most frequent combination of start station and end station trip


    print('Most commonly used combination of start station and end station trip:', df['Stations'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displaying total travel time
    print ('Total trip duration: ',df['Trip Duration'].sum())

    # Displaying mean travel time
    print('Mean trip duration: ',df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    user_type = pd.Series(df['User Type']).value_counts()
    print('User Type : \n',user_type)

    # Displaying counts of gender
    if 'Gender' in df.columns:
        gender = pd.Series(df['Gender']).value_counts()
        print('\nGender : \n',gender)
    else :
        print('Sorry no data exists on the gender type of users for the specified city')

    # Displaying earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Most earliest year of birth : ',int(df['Birth Year'].min()))
        print('Most recent year of birth : ',int(df['Birth Year'].max()))
        print('Most common year of birth : ',int(df['Birth Year'].mode()[0]))
    else:
        print('Sorry no data exists on the birth year of users for the specified city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # This is the function that enables user to view the raw data while on the disoplay screen
def data_view(df):

     count = 0
     while True:
         user_response = input('Would you like to see the raw data? '
                           'Enter yes or no.\n')
         if user_response == 'yes':
            print(df.iloc[count:count + 5])
            count += 5
         else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        data_view(df)
        time_stats(df)
        user_input1 = input('\nWould you like to see more? Enter yes or no. \n')
        if user_input1 != 'yes':
            restart_flag1 = input('\nPlease type in yes to proceed or no to quit\n')
            if restart_flag1.lower() != 'yes':
                break
        station_stats(df)
        user_input2 = input('\nWould you like to see more? Enter yes or no. \n')
        if user_input2 != 'yes':
            restart_flag2 = input('\nPlease type in yes to proceed or no to quit\n')
            if restart_flag2.lower() != 'yes':
                break
        trip_duration_stats(df)
        user_input3 = input('\nWould you like to see more? Enter yes or no. \n')
        if user_input3 != 'yes':
            restart_flag3 = input('\nPlease type in yes to proceed or no to quit\n')
            if restart_flag3.lower() != 'yes':
                break
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
