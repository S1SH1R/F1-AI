const container = document.querySelector('.container');
const search = document.querySelector('.search-box button');
const weatherBox = document.querySelector('.weather-box');
const weatherDeatils = document.querySelector('.weather-details');
const error404 = document.querySelector('.not-found');


search.addEventListener('click', () => {
    const APIKey = 
    const city = document.querySelector('.search-box input').value;

    if (city === '') {
        alert('Please enter a city name');
        return;
    }
    fetch(APIkey)
)