item = soup.find('div', {'data-component-type': 's-search-result'})
    if item:
        title = item.h2.text
        image = item.img['src']
        link = "https://amazon.in" + item.h2.a['href'].split("?")[0] + f"?tag={AFFILIATE_ID}"
        price = item.find('span', {'class': 'a-price-whole'})
        bot.send_photo(m.chat.id, image, f"ðŸ›ï¸ {title}
ðŸ’° Price: â‚¹{price.text if price else 'N/A'}
ðŸ”— {link}")
    else:
        bot.send_message(m.chat.id, "âŒ Product not found.")

# === AI CHAT ===
@bot.message_handler(func=lambda m: m.text=="ðŸ¤– AI Chat")
def aichat(m):
    msg = bot.send_message(m.chat.id, "ðŸ’¬ Send your question for AI:")
    bot.register_next_step_handler(msg, chat_response)

def chat_response(m):
    res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content": m.text}])
    bot.send_message(m.chat.id, res['choices'][0]['message']['content'])

# === AI IMAGE ===
@bot.message_handler(func=lambda m: m.text=="ðŸŽ¨ AI Image")
def aiimg(m):
    msg = bot.send_message(m.chat.id, "ðŸ–¼ï¸ Send prompt for image:")
    bot.register_next_step_handler(msg, imggen)

def imggen(m):
    res = openai.Image.create(prompt=m.text, n=1, size="512x512")
    bot.send_photo(m.chat.id, res['data'][0]['url'])

# === WITHDRAW ===
@bot.message_handler(func=lambda m: m.text=="ðŸ“¤ Withdraw")
def withdraw(m):
    cursor.execute("SELECT coins FROM users WHERE id=?", (m.chat.id,))
    bal = cursor.fetchone()[0]
    bot.send_message(m.chat.id, f"ðŸ’¼ Your balance: {bal} $ND
To withdraw, contact @YourUsername")

# === RUN THE BOT ===
bot.polling()
