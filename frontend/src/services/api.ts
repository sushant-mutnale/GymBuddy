/**
 * API Service for communicating with the GymBuddy backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchHealth() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
}

export async function fetchRoot() {
    const response = await fetch(`${API_BASE_URL}/`);
    return response.json();
}
