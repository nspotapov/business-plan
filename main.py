import numpy as np
import matplotlib.pyplot as plt
import random

random.seed(42)

# Вероятности получения заказов и их стоимости
prices = {
    'wedding_video_hourly': (1500, 5000),
    'wedding_video_daily': (30000, 60000),
    'wedding_photo': (3000, 5000),
    'kindergarten_event': (3000, 5000),
    'school_graduation': (5000, 7000),
    'business_promo': (10000, 100000)
}

# индекс узнаваемости
prestige = 1


def prestige_growth_rate():
    return 1 + (1 if random.random() > 0.2 else -1) * random.randint(1, 10) / 3000


# Вероятности заказов по месяцам (летом свадеб больше)
wedding_prob = {6: 0.3, 7: 0.35, 8: 0.3}
default_wedding_prob = 0.15

# Количество свадеб в первый месяц и рост узнаваемости
initial_weddings_per_month = 6
wedding_growth_rate = 1.05

# Количество других мероприятий в месяц
kindergarten_events_per_month = 4
school_graduation_per_month = {5: 6, 6: 4, 9: 5}
business_promo_per_month = 1


def kindergarten_events_per_month_prob(month):
    if month < 6:
        return random.expovariate(month + 3)
    elif 5 < month < 9:
        return random.expovariate(10)
    else:
        return random.expovariate(12 - month + 3)


def get_random_price(price_range):
    return random.randint(price_range[0], price_range[1])


def get_random_duration(event_type):
    durations = {
        'wedding_video_hourly': [2, 4, 6, 8],
        'wedding_video_daily': [8],
        'kindergarten_event': [2],
        'school_graduation': [4],
        'business_promo': [2, 4, 6]
    }
    return random.choice(durations[event_type])


def simulate_monthly_revenue(month):
    global prestige
    month = (month - 1) % 12 + 1

    revenue = 0
    event_counts = {'wedding': 0, 'kindergarten': 0,
                    'graduation': 0, 'business': 0}

    # Определяем вероятность свадеб в текущем месяце
    wedding_probability = wedding_prob.get(month, default_wedding_prob)
    max_weddings = round(initial_weddings_per_month *
                         (wedding_growth_rate ** month))
    weddings = min(np.random.binomial(
        max_weddings, wedding_probability), max_weddings)

    weddings_count = round(weddings * prestige)

    event_counts['wedding'] += weddings_count

    kindergarten_count = round(kindergarten_events_per_month *
                               kindergarten_events_per_month_prob(month) * prestige)

    school_count = round(school_graduation_per_month.get(month, 0) * prestige)

    business_count = round(business_promo_per_month * prestige)

    for _ in range(weddings_count):
        prestige *= prestige_growth_rate()
        if random.random() < 0.5:
            revenue += get_random_price(prices['wedding_video_daily'])
        else:
            hours = get_random_duration('wedding_video_hourly')
            revenue += hours * get_random_price(prices['wedding_video_hourly'])
        revenue += get_random_price(prices['wedding_photo'])

    # Другие мероприятия
    for _ in range(kindergarten_count):
        prestige *= prestige_growth_rate()
        event_counts['kindergarten'] += 1
        revenue += get_random_price(prices['kindergarten_event'])

    for _ in range(school_count):
        prestige *= prestige_growth_rate()
        event_counts['graduation'] += 1
        revenue += get_random_price(prices['school_graduation'])

    for _ in range(business_count):
        prestige *= prestige_growth_rate()
        event_counts['business'] += 1
        revenue += get_random_price(prices['business_promo'])

    return revenue, event_counts


def get_expense(month):
    expense = 0
    if month < 12 * 5 + 1:
        expense += 113050
    if month > 5:
        expense += 367000
    return expense


def simulate_yearly_revenue(years=1):
    months = list(range(1, 13 * years))
    revenues = []
    expenses = []
    profits = []
    event_data = {'wedding': [], 'kindergarten': [],
                  'graduation': [], 'business': []}

    for month in months:
        print(prestige)
        rev, events = simulate_monthly_revenue(month)
        revenues.append(rev)
        expenses.append(get_expense(month))
        profits.append(rev - get_expense(month))
        for key in event_data:
            event_data[key].append(events[key])

    return months, revenues, event_data, expenses, profits


# Запуск симуляции
months, revenues, event_data, expenses, profits = simulate_yearly_revenue(8)

# График выручки
plt.figure(figsize=(12, 5))
plt.plot(months, revenues, marker='o',
         linestyle='-', color='b', label='Выручка')
plt.plot(months, expenses, marker='o',
         linestyle='-', color='r', label='Издержки')
plt.plot(months, profits, marker='o',
         linestyle='-', color='g', label='Прибыль')
plt.xlabel('Месяц')
plt.ylabel('руб')
plt.title('Финансы')
plt.legend()
plt.grid()
plt.show()

# График количества мероприятий по типу
plt.figure(figsize=(12, 5))
bars = plt.bar(months, event_data['wedding'],
               color='r', alpha=0.6, label='Свадьбы')
plt.bar(months, event_data['kindergarten'],
        bottom=event_data['wedding'], color='g', alpha=0.6, label='Утренники')
plt.bar(months, event_data['graduation'], bottom=np.array(event_data['wedding']) +
        np.array(event_data['kindergarten']), color='b', alpha=0.6, label='Выпускные')
plt.bar(months, event_data['business'], bottom=np.array(event_data['wedding']) + np.array(
    event_data['kindergarten']) + np.array(event_data['graduation']), color='y', alpha=0.6, label='Реклама для бизнеса')
plt.xlabel('Месяц')
plt.ylabel('Количество мероприятий')
plt.title('Количество мероприятий по типам')
plt.legend()
plt.grid()
plt.show()
