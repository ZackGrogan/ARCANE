import React, { useState } from 'react';

interface TooltipProps {
  content: string;
  children: React.ReactNode;
}

export const Tooltip: React.FC<TooltipProps> = ({ content, children }) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onFocus={() => setIsVisible(true)}
        onBlur={() => setIsVisible(false)}
      >
        {children}
      </div>
      {isVisible && (
        <div className="absolute z-50 w-64 px-2 py-1 -mt-1 text-sm text-white transform -translate-x-1/2 bg-gray-900 rounded-lg shadow-lg left-1/2">
          {content}
          <div className="absolute w-2 h-2 transform rotate-45 bg-gray-900 -top-1 left-1/2 -translate-x-1/2"></div>
        </div>
      )}
    </div>
  );
};
