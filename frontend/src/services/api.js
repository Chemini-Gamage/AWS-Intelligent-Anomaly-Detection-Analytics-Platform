//API SERVICE
import axios from "axios";

const api = axios.create({
    //should be the api gateway url 
    baseURL: "http://127.0.0.1:8000"
});

export default api;