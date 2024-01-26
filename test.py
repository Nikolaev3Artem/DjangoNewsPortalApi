
chosen_news = 'Florida looks to keep k3122ids off social media. Can it work?'
temp_url = ''
for var in chosen_news.split()[0:4]:
    if var.isalnum() or var == '-':
        temp_url += '-' + var 
chosen_news = temp_url.lower().replace(' ','-')

print(chosen_news[1::])