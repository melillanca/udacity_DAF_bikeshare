import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH = {1: 'january',
         2: 'february',
         3: 'march',
         4: 'april',
         5: 'may',
         6: 'june',
         7: 'july',
         8: 'august',
         9: 'september',
         10: 'october',
         11: 'november',
         12: 'december'}
DAYOFWEEK = {0: 'monday',
             1: 'tuesday',
             2: 'wednesday',
             3: 'thursday',
             4: 'friday',
             5: 'saturday',
             6: 'sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    input('We need you specify us some details: [ENTER]')

    city = input('City (you can input the number or name). (1)Chicago   (2)New York   (3)Washington: ')
    city = city.lower().strip()
    while not(city in ('1', '2', '3') or city in ('chicago', 'new york', 'washington')):
        city = input('Incorrect option, try again ((1) Chicago   (2) New York   (3) Washington): ')
        city = city.lower().strip()
    if city == '1':
        city = 'chicago'
    elif city in ('2', 'new york'):
        city = 'new york city'
    elif city == '3':
        city = 'washington'

    month = input('Month [January to December OR 1 to 12]; 0 or \'all\' for all: ')
    month = month.lower().strip()
    ok_month = False
    while True:
        if month.isdigit():
            if int(month) in range(0, 13):
                break
        elif month=='all':
            month = '0'
            break
        else:
            for i in MONTH:
                if MONTH[i] == month:
                    month = str(i)
                    ok_month = True
                    break
            if ok_month:
                break
        month = input('Incorrect option, try again (Month [January to December OR 1 to 12]; 0 or \'all\' for all): ')

    """
    Pandas list the days of the week from 0 to 6. Here it is listed from 1 to 7 to make
    things easier for the user, then internally it adapts to the numbering of Pandas.
    """
    day = input('Day of week (you can input the number or name). (1) Monday    (2) Tuesday    (3) Wednesday    (4) Thursday    (5) Friday    (6) Saturday    (7) Sunday    (0) All: ')
    day = day.lower().strip()
    while not day in ('1', '2', '3', '4', '5', '6', '7', '0', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        day = input('Incorrect option, try again ((1)Monday   (2)Tuesday   (3)Wednesday   (4)Thursday   (5)Friday   (6)Saturday   (7)Sunday   (0)All): ')
        day = day.lower().strip()
    if day in ('1', '2', '3', '4', '5', '6', '7', '0'):
        day = str(int(day) - 1)
    elif day == 'all':
        day = '-1'
    else:
        for i in DAYOFWEEK:
            if DAYOFWEEK[i] == day:
                day = str(i)

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
    month = int(month)
    day = int(day)

    df = pd.read_csv(CITY_DATA[city], parse_dates=["Start Time", "End Time"])

    if month != 0:
        month_selected = df['Start Time'].dt.month == month
        df = df[month_selected]
    if day != -1:
        dayweek = df['Start Time'].dt.weekday == day
        df = df[dayweek]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('{} is the most common month.'.format(MONTH[df['Start Time'].dt.month.mode()[0]]).capitalize())

    print('{} is the most common day of week.'.format(DAYOFWEEK[df['Start Time'].dt.dayofweek.mode()[0]]).capitalize())

    print('The most common hour is {}.'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('{} is the most commonly used start station.'.format(df['Start Station'].mode()[0]))

    print('The most commonly used end station is {}.'.format(df['End Station'].mode()[0]))

    df['combination'] = df['Start Station'] + ' - ' + df['End Station']
    print('{} is the most frequent combination of start station and end station trip.'
          .format(df['combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total travel time was {}.'.format(str((df['End Time'] - df['Start Time']).sum())))


    print('Mean travel time was {}.'.format(str((df['End Time'] - df['Start Time']).mean())))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    usertype_df = df.groupby(['User Type']).count()
    for index, row in usertype_df.head().iterrows():
        print('There are {} users of {} type.'.format(row[0], index))

    if 'Gender' in df:
        gender_df = df.groupby(['Gender']).count()
        for index, row in gender_df.head().iterrows():
            print('{} users are {}.'.format(row[0], index).capitalize())

    if 'Birth Year' in df:
        print('Earliest year of birth is {}, the most recent is {}; and the most common is {}.'.format(
            int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    index = 0
    user_input = input('Do you want to display more 5 rows of raw data? ').lower()
    while user_input in ['yes', 'y', 'yep', 'yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('Do you want to display more 5 rows of raw data?').lower()


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
        if restart.lower() not in('yes', 'y', 'yep', 'yea'):
            break


if __name__ == "__main__":
    main()
