import './App.css';
import { useState } from 'react';
import axios from 'axios';



export default function MyApp() {
    const [topic, setTopic] = useState('');
    const [headline, setHeadline] = useState(null);
    const [loading, setLoading] = useState(false);
    //const [list, setList] = useState([])

    const handleSubmit = async (e) => {
      e.preventDefault(); 
      setLoading(true);
      try{
        const response = await axios.post('http://localhost:8000/topic', { topic });
        console.log("Response from FastAPI", response.data);
        setHeadline(response.data.headlines);

      }
      catch(error){
        console.error(error);
      }finally{
        setLoading(false)
      }
    }
    return (
      <div className = "input" class="h-[100vh] flex flex-col justify-between ">
          <div class="title font-serif text-9xl ">
            <h1>Guardian AI</h1>
          </div>
        <div class="flex flex-col items-center">
        <div class="w-full max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-6 md:p-8 dark:bg-gray-800 dark:border-gray-700 ">
        <form 
          onSubmit = {handleSubmit}
          class = "flex flex-col items-center space-y-4"
        >
            <label>
              Enter the Topic for 360 News : 
            </label>
            <input 
                type="text"
                value = {topic}
                onChange = {(e) => setTopic(e.target.value)}
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
            />
            <button 
              class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              type = "submit">
              Give
            </button>
        </form>
        </div>
        <div >
        {loading && <p>Loading...</p>}
        </div>
        <div>
        {headline && (
          <div class="text-lg">
            <p><strong> <a href={headline.positive} target='blank'>Click for Positive Headline</a></strong></p>
            <p><strong> <a href={headline.negative} target='blank'>Click for Negative Headline</a></strong></p>
            <p><strong> <a href={headline.neutral} target='blank'>Click for Neutral Headline</a></strong></p>
          </div>
        )}
        </div>
        </div>
          <div class="footer text-center text-lg">
              <p>Guardian AI can make mistakes and not give results in which case you may refresh the website</p>
          </div>
      </div>
    );
}




