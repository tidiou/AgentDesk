import { Routes, Route } from 'react-router-dom'
import MainApp from './MainApp'
import SharedAnalyticsView from './pages/SharedAnalyticsView'

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainApp />} />
      <Route path="/share/:shareId" element={<SharedAnalyticsView />} />
    </Routes>
  )
}

export default App