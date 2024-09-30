# 🎬 Movie Recommendation Website

A **Django-based** movie recommendation platform featuring a hybrid recommendation system that combines **content similarity search** using **ChromaDB** and **matrix factorization collaborative filtering** for personalized movie recommendations. The website includes real-time search suggestions, multi-device login, and session management for a personalized user experience.

![Movie Recommendation Website Screenshot](/demo/img0.png)![Movie Recommendation Website Screenshot](/demo/img1.png)![Movie Recommendation Website Screenshot](/demo/img2.png)

## 🚀 Features

- **Hybrid Recommendation System**:
  - **Content-based filtering** powered by **SBERT embeddings** stored in **ChromaDB**.
  - **Collaborative filtering** using matrix factorization implemented in **PyTorch**.
- **Real-time Search Suggestions**:

  - Get search suggestions as you type, based on movie titles names.

- **User Management**:
  - Users can log in to a maximum of **3 devices** at a time.
  - Automatic logout from all devices if the user resets their password.

- **Custom Movie Database**:
  - Contains **16,000+ movies** and **1,400 users**.

- **Load On Scroll**:
  - Movies Load on Scroll.

- **Add To Mylist**:
    - User add/remove movies to list.

- **Trending Now**:
    - Movies watched by max number users of last week.

- **Payment System**:
    - Use a paytm payment gateway.

## 🐞 Known Bugs & Issues

- **Multi-device Recommendations**:
  - The system currently recommends the same movies across all devices logged in with the same user account. Personalization per device is **not supported yet**.
- **UI Interaction Bugs**:
  - Some UI elements may behave inconsistently across different browsers or screen sizes.
- **Performance Optimization**:

  - The recommendation system can be further optimized for **faster load times** and **better scalability** with large datasets.

- **Responsive UI**:
  - Design for desktop only. But work slightly for mobile views (with known bugs, see below).

- **Missing Poster**:
    - Some movies has no images.

## 📂 Demo

### Video

[![Watch the video]](https://github.com/user-attachments/assets/acad1f4d-fa0b-429c-be11-e35542fc0fce)


## ⚙️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/VachhaniJanak/movie_recommendation_website.git
   ```

2. **Install dependencies**:

   ```bash
   cd movie_recommendation_website/
   pip install -r requirements.txt # "For CPU base linux machine."
   ```

3. **Start the server**:
   ```bash
   cd movies_recom
   python manage.py runserver
   ```

## 🔧 Technologies Used

- **Backend**: Django, PyTorch
- **Content Similarity**: ChromaDB with SBERT embeddings
- **Collaborative Filtering**: Matrix Factorization in PyTorch
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLLite
- **Authentication**: Django sessions with multi-device login restrictions

## 📈 Future Enhancements

- **Per-device Recommendations**: Ensure personalized movie recommendations on each logged-in device.
- **UI/UX Enhancements**: Fix UI bugs for a smoother user experience across all devices.
- **Performance Optimization**: Optimize database queries and recommendation algorithms for better scalability.


