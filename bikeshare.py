import time
import pandas as pd



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

    # get user input for city (chicago, new york city, washington)
    city = input('Enter the city you want see data for Chicago , New York City or Washington : ')
    city = city.casefold()
    while city not in CITY_DATA:
        city = input('Invalid city name.Please Try Again!')
        city = city.casefold()

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Enter the month from January to June OR Enter "all" for no month filter : ')
    month = month.casefold()
    while month not in months:
        month = input('Invalid month name.Please Try Again!')
        month = month.casefold()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Enter the day from Monday to Sunday OR Enter "all" for no day filter : ')
    day = day.casefold()
    while day not in days:
        day = input('Invalid day name.Please Try Again!')
        day = day.casefold()

    print('='*50)
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
    # Loading data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filtering by month if applicable
    if month != 'all':
        # Useing the index of the months list to get corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filtering by month to create new dataframe
        df = df[df['month'] == month]

    # Filtering by day of week if applicable
    if day != 'all':
        # Filtering by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Popular Month:', months[popular_month-1])

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    popular_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('Most Popular Day:', days[popular_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Popular Start Station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Popular End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('\nMost Frequent Combination of Start and End Station Trips:\n\n',df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Trip Duration:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean Trip Duration:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender,'\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', df['Birth Year'].min())
        print('Most Recent year of Birth:', df['Birth Year'].max())
        print('Most Common year of Birth:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*50)
def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    enter = ['yes', 'no']
    user_input = input('\nWould you like to see the raw data? (Enter: Yes/No).\n').lower()
    while user_input not in enter:
        user_input = input('Please Enter Yes or No:\n').lower()

    n = 0
    while user_input == 'yes':
        # Print the next 5 rows
        print(df.iloc[n : n + 5])
        n += 5

        # Check whether all the data has been shown BEFORE asking again
        if n >= len(df):
            print('\nYou have reached the end of the data.')
            break

        # Data still remains, so ask whether to continue
        user_input = input('\nWould you like to see more data? (Enter: Yes/No).\n').lower()
        while user_input not in enter:
            user_input = input('Please Enter Yes or No:\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print('\nThere is no data for the filters you selected '
                  '(city: {}, month: {}, day: {}).'.format(city, month, day))
            print('Please try a different combination.')
            print('='*50)
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df) 

            # To prompt the user whether they would like to see the raw data
        enter = ['yes', 'no']
        restart = input('\nWould you like to restart? (Enter: Yes/No).\n').lower()
        while restart not in enter:
            restart = input('Please Enter Yes or No:\n').lower()
        if restart != 'yes':
            print('BYE!')
            break

if __name__ == "__main__":
	main()