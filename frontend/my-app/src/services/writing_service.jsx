import axios from 'axios';

export async function GrammarCheck(text) {
  try {
    const { data } = await axios.post('http://localhost:8000/grammar-check', {
      text
    });
    console.log('Check grammar completely');
    return data;
  } catch (error) {
    console.error('Error checking grammar:', error);
  }
}

export async function AnalyzeLevel(text) {
  try {
    const { data } = await axios.post('http://localhost:8000/level-analysis', {
      text
    });
    console.log('Analyze level completely');
    return data;
  } catch (error) {
    console.error('Error analyzing level:', error);
  }
}


export async function WritingFeedback(text) {
  try {
    const { data } = await axios.post('http://localhost:8000/writing-feedback', {
      text
    });
    console.log('Feedback completely');
    return data;
  } catch (error) {
    console.error('Error feedbacking:', error);
  }
}


export async function VocabularySupport(text) {
  try {
    const { data } = await axios.post(`http://localhost:8000/vocabulary?text=${encodeURIComponent(text)}`);

    console.log('Support Vocabulary completely');
    return data;
  } catch (error) {
    console.error('Error support vocabulary:', error);
  }
}