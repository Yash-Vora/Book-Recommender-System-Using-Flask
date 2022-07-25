from flask import Flask, render_template, request
import pickle


with open('popular_books.pkl', 'rb') as f:
    popular_books = pickle.load(f)

with open('pt.pkl', 'rb') as f:
    pt = pickle.load(f)

with open('similarity_score.pkl', 'rb') as f:
    similarity_score = pickle.load(f)

with open('books.pkl', 'rb') as f:
    books = pickle.load(f)

with open('avg_ratings.pkl', 'rb') as f:
    avg_ratings = pickle.load(f)


app = Flask('__main__')


@app.route('/')
def home():
    return render_template('index.html',
                            image_url = list(popular_books['Image-URL-M'].values),
                            book_name = list(popular_books['Book-Title'].values),
                            book_author = list(popular_books['Book-Author'].values),
                            votes = list(popular_books['Num-Ratings'].values),
                            avg_ratings = [round(i, 2) for i in list(popular_books['Avg-Ratings'].values)]
                            )


@app.route('/recommendation')
def recommendation():
    return render_template('recommend.html')


@app.route('/recommend_book', methods=['POST'])
def recommend_book():
    user_input = request.form.get('recommend_books')

    recommended_books = []
    
    index = list(pt.index).index(user_input)
    similar_books = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1], reverse=True)[1:6]
    
    for book in similar_books:
        item = {}
        temp_df = books[books['Book-Title'] == pt.index[book[0]]].drop_duplicates('Book-Title')
        item['Book_Name'] = temp_df['Book-Title'].iloc[0]
        item['Book_Author'] = temp_df['Book-Author'].iloc[0]
        item['Image_URL'] = temp_df['Image-URL-M'].iloc[0]
        item['Book_Ratings'] = round(avg_ratings[avg_ratings['Book-Title'] == pt.index[book[0]]]['Avg-Ratings'].iloc[0], 2)
        
        recommended_books.append(item)

    return render_template('recommend.html', user_input = user_input, recommended_books=recommended_books)


if __name__ == '__main__':
    app.run(debug=True)