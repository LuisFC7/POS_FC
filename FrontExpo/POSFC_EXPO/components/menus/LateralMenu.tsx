import React, { useState } from "react";
import { View, Text, TouchableOpacity } from "react-native";
import tw from "tailwind-react-native-classnames";
 // Importamos Tailwind para React Native

interface MenuItem {
  label: string;
  onPress?: () => void;
  subItems?: MenuItem[];
}

interface LateralMenuProps {
  items: MenuItem[];
}

const LateralMenu: React.FC<LateralMenuProps> = ({ items }) => {
  const [openMenus, setOpenMenus] = useState<{ [key: string]: boolean }>({});

  const toggleSubMenu = (label: string) => {
    setOpenMenus((prev) => ({
      ...prev,
      [label]: !prev[label],
    }));
  };

  return (
    <View style={tw`p-4 bg-gray-100`}>
      {items.map((item, index) => (
        <View key={index}>
          <TouchableOpacity
            style={tw`p-4 bg-blue-500 rounded-md my-2`}
            onPress={item.subItems ? () => toggleSubMenu(item.label) : item.onPress}
          >
            <Text style={tw`text-white font-bold`}>{item.label}</Text>
          </TouchableOpacity>

          {/* Mostrar submenú si está abierto */}
          {item.subItems && openMenus[item.label] && (
            <View style={tw`ml-4 mt-2`}>
              {item.subItems.map((subItem, subIndex) => (
                <TouchableOpacity
                  key={subIndex}
                  style={tw`p-3 bg-blue-700 rounded-md my-1`}
                  onPress={subItem.onPress}
                >
                  <Text style={tw`text-white`}>{subItem.label}</Text>
                </TouchableOpacity>
              ))}
            </View>
          )}
        </View>
      ))}
    </View>
  );
};

export default LateralMenu;
