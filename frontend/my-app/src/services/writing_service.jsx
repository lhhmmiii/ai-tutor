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

export async function grammar_check(user_id, text) {
  try {
    const { data } = await  axios.post(`${API_BASE_URL}/grammar?user_id=${user_id}&text=${encodeURIComponent(text)}`, {}, getAuthHeader());
    console.log('Check grammar completely');
    return data;
  } catch (error) {
    console.error('Error checking grammar:', error);
  }
}

export async function AnalyzeLevel(text) {
  try {
    const { data } = await axios.post(`${API_BASE_URL}/level-analysis`, { text }, getAuthHeader());
    console.log('Analyze level completely');
    return data;
  } catch (error) {
    console.error('Error analyzing level:', error);
  }
}

export async function WritingFeedback(text) {
  try {
    const { data } = await axios.post(`${API_BASE_URL}/writing-feedback`, { text }, getAuthHeader());
    console.log('Feedback completely');
    return data;
  } catch (error) {
    console.error('Error feedbacking:', error);
  }
}

export async function VocabularySupport(text) {
  try {
    const { data } = await axios.get(`${API_BASE_URL}/vocabulary?text=${encodeURIComponent(text)}`, getAuthHeader());
    console.log('Support Vocabulary completely');
    return data;
  } catch (error) {
    console.error('Error support vocabulary:', error);
  }
}

export async function WritingAgent(userId, question) {
  try {
    const requestBody = {
      user_id: userId,
      question: question,
    };

    const { data } = await axios.post(`${API_BASE_URL}/writing_agent`, requestBody, getAuthHeader());
    console.log('Chatbot response received');
    return data;
  } catch (error) {
    console.error('Error calling Writing Agent:', error);
    throw error;
  }
}
