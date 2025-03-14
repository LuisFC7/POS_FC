import axios from "axios";


const API_URL = "http://127.0.0.1:8000/home/";

export const getMenuData = async () => {
  try {
    const response = await axios.get(API_URL, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error("Error al obtener el menú:", error);
    return null; 
  }
};
