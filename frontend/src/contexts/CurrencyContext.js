import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const CurrencyContext = createContext();

export const useCurrency = () => {
  const context = useContext(CurrencyContext);
  if (!context) {
    throw new Error('useCurrency must be used within CurrencyProvider');
  }
  return context;
};

export const CurrencyProvider = ({ children }) => {
  const [currencySymbol, setCurrencySymbol] = useState('$');
  const [currencyCode, setCurrencyCode] = useState('USD');
  const { API, getAuthHeader, user } = useAuth();

  useEffect(() => {
    if (user) {
      fetchSettings();
    }
  }, [user]);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API}/settings`, { headers: getAuthHeader() });
      setCurrencySymbol(response.data.currency_symbol);
      setCurrencyCode(response.data.currency_code);
    } catch (error) {
      console.error('Failed to fetch settings', error);
    }
  };

  const formatPrice = (price) => {
    return `${currencySymbol}${price.toFixed(2)}`;
  };

  const updateCurrency = async (symbol, code) => {
    try {
      await axios.put(`${API}/settings`, 
        { currency_symbol: symbol, currency_code: code },
        { headers: getAuthHeader() }
      );
      setCurrencySymbol(symbol);
      setCurrencyCode(code);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Failed to update currency' };
    }
  };

  return (
    <CurrencyContext.Provider value={{ 
      currencySymbol, 
      currencyCode, 
      formatPrice, 
      updateCurrency,
      refreshSettings: fetchSettings 
    }}>
      {children}
    </CurrencyContext.Provider>
  );
};
