import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import NPCForm from '@/components/NPCForm';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('NPCForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders all form fields', () => {
    render(<NPCForm />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/race/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/class/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/background/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/alignment/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/personality traits/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/backstory/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/appearance/i)).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(<NPCForm />);
    
    const submitButton = screen.getByRole('button', { name: /create/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/race is required/i)).toBeInTheDocument();
      expect(screen.getByText(/class is required/i)).toBeInTheDocument();
    });
  });

  it('successfully submits form data', async () => {
    const mockNPC = {
      name: 'Test NPC',
      race: 'Human',
      class: 'Fighter',
      background: 'Soldier',
      alignment: 'Lawful Good',
      personalityTraits: 'Brave',
      backstory: 'A veteran',
      appearance: 'Tall',
      skills: ['Athletics'],
      equipment: ['Sword'],
    };

    mockedAxios.post.mockResolvedValueOnce({ data: mockNPC });

    render(<NPCForm />);
    
    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: mockNPC.name } });
    fireEvent.change(screen.getByLabelText(/race/i), { target: { value: mockNPC.race } });
    fireEvent.change(screen.getByLabelText(/class/i), { target: { value: mockNPC.class } });
    fireEvent.change(screen.getByLabelText(/background/i), { target: { value: mockNPC.background } });
    fireEvent.change(screen.getByLabelText(/alignment/i), { target: { value: mockNPC.alignment } });
    fireEvent.change(screen.getByLabelText(/personality traits/i), { target: { value: mockNPC.personalityTraits } });
    fireEvent.change(screen.getByLabelText(/backstory/i), { target: { value: mockNPC.backstory } });
    fireEvent.change(screen.getByLabelText(/appearance/i), { target: { value: mockNPC.appearance } });

    const submitButton = screen.getByRole('button', { name: /create/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledWith('/api/npcs/create', mockNPC);
    });
  });

  it('handles API errors', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('API Error'));

    render(<NPCForm />);
    
    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Test' } });
    fireEvent.change(screen.getByLabelText(/race/i), { target: { value: 'Human' } });
    fireEvent.change(screen.getByLabelText(/class/i), { target: { value: 'Fighter' } });

    const submitButton = screen.getByRole('button', { name: /create/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/error creating npc/i)).toBeInTheDocument();
    });
  });
});
