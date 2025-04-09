import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

export const getProductos = () => axios.get(`${API_URL}/productos`);
export const createProducto = (producto) => axios.post(`${API_URL}/productos`, producto);
export const deleteProducto = (id) => axios.delete(`${API_URL}/productos/${id}`);