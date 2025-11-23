// frontend/lib/api.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  // Check health
  async checkHealth() {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.json();
  },

  // Upload video
  async uploadVideo(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/video/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload video');
    }

    return response.json();
  },

  // Create campaign from transcript
  async createCampaign(transcript: string, metadata = {}) {
    const response = await fetch(`${API_BASE_URL}/api/campaign/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        transcript,
        video_metadata: metadata,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to create campaign');
    }

    return response.json();
  },

  // Create campaign from manual transcript
  async createCampaignFromTranscript(transcript: string, videoTitle = "Manual Input") {
    const response = await fetch(`${API_BASE_URL}/api/campaign/from-transcript`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        transcript,
        video_title: videoTitle,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to create campaign');
    }

    return response.json();
  },
};