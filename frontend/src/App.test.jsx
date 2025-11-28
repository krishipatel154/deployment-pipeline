import { render, screen } from '@testing-library/react'
import App from './App'

test('renders signup heading', () => {
  render(<App />)
  expect(screen.getByText(/create your account/i)).toBeInTheDocument()
})
