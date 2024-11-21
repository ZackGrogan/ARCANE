import { Transition as HeadlessTransition } from '@headlessui/react';
import { Fragment, ReactNode } from 'react';

interface TransitionProps {
  show: boolean;
  appear?: boolean;
  children: ReactNode;
  as?: any;
}

export const Transition = ({
  show,
  appear,
  children,
  as = Fragment,
  ...props
}: TransitionProps) => {
  return (
    <HeadlessTransition
      show={show}
      appear={appear}
      as={as}
      {...props}
    >
      {children}
    </HeadlessTransition>
  );
};

// Re-export Child component from HeadlessUI
Transition.Child = HeadlessTransition.Child;
