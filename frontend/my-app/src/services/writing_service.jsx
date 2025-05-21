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

////////////////////////////////////////////////////
export async function CreateVocabulary(user_id, text) {
  try {
    console.log(user_id, text)
    const { data } = await axios.post(`${API_BASE_URL}/vocabulary?user_id=${user_id}&text=${encodeURIComponent(text)}`,
                                      {}, getAuthHeader());
    console.log('Vocabulary created successfully');
    return data;
  } catch (error) {
    console.error('Error creating vocabulary:', error);
  }
}


export async function GetVocabulary(user_id) {
  try {
    const { data } = await axios.get(`${API_BASE_URL}/vocabularies?user_id=${user_id}`, getAuthHeader());
    console.log('Fetched vocabulary successfully');
    return data;
  } catch (error) {
    console.error('Error fetching vocabulary:', error);
  }
}



export async function UpdateVocabulary(user_id, word, updates) {
  try {
    const { data } = await axios.put(`${API_BASE_URL}/vocabulary?user_id=${user_id}&word=${word}`,
                                      updates, getAuthHeader());
    console.log('Vocabulary updated successfully');
    return data;
  } catch (error) {
    console.error('Error updating vocabulary:', error);
  }
}

export async function DeleteVocabulary(word_id) {
  try {
    const { data } = await axios.delete(`${API_BASE_URL}/vocabulary?word_id=${word_id}`, getAuthHeader());
    console.log('Vocabulary deleted successfully');
    return data;
  } catch (error) {
    console.error('Error deleting vocabulary:', error);
  }
}

////////////////////////////////////////////////////

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

export async function ConversationAgent(userId, question) {
  try {
    const requestBody = {
      user_id: userId,
      question: question,
    };
    const { data } = await axios.post(`${API_BASE_URL}/conversation_agent`, requestBody, getAuthHeader());
    console.log('Chatbot response received');
    return data;
  } catch (error) {
    console.error('Error calling Conversation Agent:', error);
    throw error;
  }
}
