import React, { useEffect, useState } from "react";
import { View, Text, TouchableOpacity } from "react-native";
import LateralMenu from "../../components/menus/LateralMenu";
import api from "../api/axiosConfig";
import tw from "tailwind-react-native-classnames";
import Icon from 'react-native-vector-icons/FontAwesome'; 
import AsyncStorage from '@react-native-async-storage/async-storage'; 
import { useNavigation } from '@react-navigation/native'; 

const PrincipalPage = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const navigation = useNavigation();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/home"); 
        setData(response.data);
      } catch (err) {
        setError("Error al cargar los datos");
        console.error(err);
      }
    };

    fetchData();
  }, []);

  const logout = async () => {
    try {
      
      const response = await api.post("/logout_usuario", {}, {
        withCredentials: true 
      });
  
      await AsyncStorage.removeItem('token'); 
  
      navigation.navigate('login');  
      console.log("Sesión cerrada exitosamente");
    } catch (err) {
      console.error("Error al cerrar sesión", err);
    }
  };
  

  const menuItems = [
    { label: "Inicio", onPress: () => console.log("Ir a Inicio") },
    { 
      label: "Configuración", 
      subItems: [
        { label: "Perfil", onPress: () => console.log("Ir a Perfil") },
        { label: "Seguridad", onPress: () => console.log("Ir a Seguridad") }
      ]
    },
    { label: "Ayuda", onPress: () => console.log("Ir a Ayuda") },
  ];

  return (
    <View style={tw`flex-row h-full`}>
     
      <View style={tw`w-1/4 bg-gray-200 p-4`}>
        <LateralMenu items={menuItems} />
      </View>

      <View style={tw`w-3/4 bg-white p-4`}>
        <TouchableOpacity onPress={logout} style={tw`absolute top-4 right-4`}>
          <Icon name="sign-out" size={30} color="#000" />
        </TouchableOpacity>

        {error ? <Text style={tw`text-red-500`}>{error}</Text> : null}
        {data ? <Text style={tw`text-lg font-bold`}>{data.datos}</Text> : <Text>Cargando...</Text>}
      </View>
    </View>
  );
};

export default PrincipalPage;
