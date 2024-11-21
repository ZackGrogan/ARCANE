import React, { useState } from 'react';
import { Dialog, Transition, Fragment } from '@/components/UI';
import { useAIGeneration } from '../hooks/useAIGeneration';
import { getFieldHelp, getExamplePrompts } from '../utils/aiGenerationUtils';

interface AIGenerationModalProps {
  isOpen: boolean;
  onClose: () => void;
  field: string;
  currentCharacter?: any;
  onGenerate: (content: string) => void;
}

export default function AIGenerationModal({
  isOpen,
  onClose,
  field,
  currentCharacter,
  onGenerate
}: AIGenerationModalProps) {
  const [prompt, setPrompt] = useState('');
  const { generateContent, isLoading, error } = useAIGeneration({
    field,
    currentCharacter,
    onSuccess: (content) => {
      onGenerate(content);
      onClose();
    }
  });

  const helpText = getFieldHelp(field);
  const examplePrompts = getExamplePrompts(field);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await generateContent(prompt);
  };

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">
                  Generate {field}
                </Dialog.Title>

                <div className="mt-2">
                  <p className="text-sm text-gray-500 mb-4">{helpText}</p>

                  <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                      <label htmlFor="prompt" className="block text-sm font-medium text-gray-700">
                        Custom Prompt (Optional)
                      </label>
                      <textarea
                        id="prompt"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        rows={3}
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="Enter your custom prompt here..."
                      />
                    </div>

                    {examplePrompts.length > 0 && (
                      <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Example Prompts:
                        </label>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {examplePrompts.map((example, index) => (
                            <li 
                              key={index}
                              className="cursor-pointer hover:text-indigo-600"
                              onClick={() => setPrompt(example)}
                            >
                              • {example}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {error && (
                      <div className="mb-4 text-sm text-red-600">
                        {error}
                      </div>
                    )}

                    <div className="mt-4 flex justify-end space-x-3">
                      <button
                        type="button"
                        className="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
                        onClick={onClose}
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2"
                        disabled={isLoading}
                      >
                        {isLoading ? (
                          <span className="flex items-center space-x-2">
                            <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            <span>Generating...</span>
                          </span>
                        ) : (
                          'Generate'
                        )}
                      </button>
                    </div>
                  </form>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
