const axios = require('axios');

const fetch_data = {
  get: async (url, token, data={}) => {
    try {
      const response = await axios.get(url,{
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token,
        }
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  },
  post: async (url, token, data) => {
    try {
      const response = await axios.post(url, data, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  },
  put: async (url, token, data) => {
    try {
      const response = await axios.put(url, data, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  },
  delete: async (url, token) => {
    try {
      const response = await axios.delete(url, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  }
};

module.exports = fetch_data;