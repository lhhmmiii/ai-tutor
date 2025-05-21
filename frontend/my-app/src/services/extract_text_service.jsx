import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL;

// Lấy access token từ localStorage
function getAuthHeader() {
    const token = localStorage.getItem('access_token');
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  }

  
// export async function extract_text(user_id, text) {
// try {
//     const { data } = await  axios.post(`${API_BASE_URL}/grammar?user_id=${user_id}&text=${encodeURIComponent(text)}`, {}, getAuthHeader());
//     console.log('Check grammar completely');
//     return data;
// } catch (error) {
//     console.error('Error checking grammar:', error);
// }
// }