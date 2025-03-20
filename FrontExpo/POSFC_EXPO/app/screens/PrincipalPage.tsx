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
  const [menuItems, setMenuItems] = useState([]);
  const navigation = useNavigation();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/home");
        setData(response.data);

        // Transformar la respuesta en el formato correcto para el menú
        const opciones = response.data.opciones;

        const menuMap = {}; // Para agrupar opciones
        opciones.forEach(({ Opcion, Subopcion }) => {
          if (!menuMap[Opcion]) {
            menuMap[Opcion] = { label: Opcion, subItems: [] };
          }
          if (Subopcion) {
            menuMap[Opcion].subItems.push({
              label: Subopcion,
              onPress: () => {}  // Acción vacía
            });
          }
        });
        

        // Convertir el objeto en un array
        const formattedMenu = Object.values(menuMap).map(item => ({
          label: item.label,
          ...(item.subItems.length > 0 ? { subItems: item.subItems } : { onPress: () => {} }) // Acción vacía
        }));
        

        setMenuItems(formattedMenu);
      } catch (err) {
        setError("Error al cargar los datos");
        console.error(err);
      }
    };

    fetchData();
  }, []);

  const logout = async () => {
    try {
      await api.post("/logout_usuario", {}, { withCredentials: true });
      await AsyncStorage.removeItem('token');
      navigation.navigate('login');
    } catch (err) {
      console.error("Error al cerrar sesión", err);
    }
  };

  return (
    <View style={tw`flex-row h-full`}>
      {/* Menú lateral */}
      <View style={tw`w-1/4 bg-gray-200 p-4`}>
        <LateralMenu items={menuItems} />
      </View>

      {/* Contenido principal */}
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
