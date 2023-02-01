import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters():
    """
     Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city you would like to explore : "chicago" , "new york city" , or "washington"  :').lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print(" You entered wrong choice , please try again")
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            'Enter "all" for all data or chose  a month : "january" , "february" , "march", "april" , "may" or "june "  :').lower()
        if month not in ("all", "january", "february", "march", "april", "may", "june"):
            print(" You entered wrong choice , please try again")
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter "all" for all days or chose a day : "saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday":  ').lower()
        if day not in ("all", "saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"):
            print(" You entered wrong choice , please try again")
            continue
        else:
            break

    print('-' * 60)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start_Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # New columns, month and day_of_week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':
        # use the index of the month_list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

        # filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    common_month = months[month - 1]
    print("\n The most popular month is  : ", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("\n The most popular day of the week is  : ", common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("\n The most popular hour of the day is : ",common_hour)

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*60)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('\n The most commonly used start station is :  \n', start_station)

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('\nThe most commonly used end station is:  \n', end_station)

    # display most frequent combination of start station and end station trip
    df["route"] = df["Start Station"] + "  AND  " + df["End Station"]
    combination = df['route'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip:\n', combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Total and average Times of Travel...\n')
    start_time = time.time()

    # display total travel time
    travel_time = sum(df['Trip Duration'])
    print('\nThe Total travel time is :', travel_time / (60 * 60 * 24), " Days")

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('\nThe average travel time is :', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser Types:\n', user_types)

    # TO DO: Display counts of gender
    try:
        # try to get first mode of column 'month'
        gender = df['Gender'].value_counts()
        print('\nGender counts are : ',gender)

    except KeyError:
        print('\nGender counts are : Unknown')

   # Display earliest Year
    try:
        earliest_year = df['Birth Year'].min()
        print('\nThe earliest birth year is:  ', earliest_year)
    except KeyError:
        print('\nThe earliest birth year is: Unknown ')

  #Display most recent Year
    try:
        most_year = df['Birth Year'].max()
        print('\nThe most recent birth year is:  ', most_year)
    except KeyError:
        print('\nThe most recent birth year is: Unknown ')

    # Display most common year of birth
    try:
        common_year = df['Birth Year'].mode()[0]
        print('\nThe most common birth year is:  ', common_year)
    except KeyError:
         print('\nThe most common birth year is: Unknown ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter 'yes ' or ' no' : ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()