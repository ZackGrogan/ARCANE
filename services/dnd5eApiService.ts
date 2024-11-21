import axios from 'axios';

const DND5E_API_BASE_URL = 'https://www.dnd5eapi.co/api';

export const fetchMonsterStats = async (monsterName: string) => {
  try {
    const response = await axios.get(`${DND5E_API_BASE_URL}/monsters/${monsterName}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching monster stats:', error);
    throw error;
  }
};

export const fetchItemDetails = async (itemName: string) => {
  try {
    const response = await axios.get(`${DND5E_API_BASE_URL}/equipment/${itemName}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching item details:', error);
    throw error;
  }
};

export const fetchSpellDetails = async (spellName: string) => {
  try {
    const response = await axios.get(`${DND5E_API_BASE_URL}/spells/${spellName}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching spell details:', error);
    throw error;
  }
};
