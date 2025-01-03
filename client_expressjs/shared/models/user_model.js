const axios = require('axios');
require('dotenv').config();
const userAPI = process.env.API_SERVER + "users/";

user_model = {
    login: async (email, password) => {
        try {
            const response = await axios.post(userAPI + 'login', {
                email: email,
                password: password
            }, {
                headers: { 'Content-Type': 'application/json' }
            });
            return response.data; 
        } catch (error) {
            return error; 
        }
    },
    get_profile: async (token) => {
        try {
            const response = await axios.post(userAPI + 'profile', {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${token}`
                }
            });
            return response.data; // Return the data when the Promise resolves
        } catch (error) {
            console.error("Error fetching profile:", error);
            throw error; // Re-throw to handle the error in the calling function
        }
    },
    get_account: async (token) => { 
        try {
            const response = await axios.post(userAPI + 'account', {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${token}`
                }
            });
            return response.data; // Return the data when the Promise resolves
        } catch (error) {
            console.error("Error fetching profile:", error);
            throw error; // Re-throw to handle the error in the calling function
        }
    }
}

module.exports = user_model;
