


import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute.jsx';
import Home from './pages/Home/Home';
import Navbar from './components/Navbar/Navbar';
import BookDetails from './pages/BookDetails/BookDetails';
import Layout from './components/Layout/Layout';
import Borrowed from './pages/Borrowed/Borrowed';
import FillUpForm from './components/FillUpForm/FillUpForm';
import Dashboard from './pages/Dashboad/Dashboad';
import UploadBookPage from './components/Upload/UploadBookPage';
import AllGenres from './pages/AllGenres/AllGenres';
import ManageBooks from './pages/ManageBooks/ManageBooks';
import ManageCategory from './pages/ManageCategory/ManageCategory';
import UserDashboard from './pages/User/UserDashboard';
import MyLoansBlank from './pages/MyLoansBlank/MyLoansBlank';
import UserSettings from './pages/UserSettings/UserSettings';
import UserHistory from './pages/UserHistory/UserHistory';
import AdminSettings from './pages/AdminSettings/AdminSettings';
import AdminHistory  from './pages/AdminSettings/AdminHistory';
import ManageFeature from './pages/ManageFeature/ManageFeature';
import DonationRequest from './pages/DonationRequest/DonationRequest';
import AuthGate from './pages/AuthGate/AuthGate';
import CalendarPage from './pages/Calendar/CalendarPage';
import Login from './pages/Auth/Login';

function AppContent() {
  const location = useLocation();
  const hideLayoutPaths = ["/login"];
  const hideLayout = hideLayoutPaths.includes(location.pathname);

  return (
    <>
      {!hideLayout && <Navbar />}

      <main className="flex-grow">
        <Routes>
          <Route path="/login" element={<Login />} />
          {!hideLayout && (
            <Route element={<Layout />}>
              <Route path="/" element={<Home />} />
              <Route path="/book/:id" element={ <ProtectedRoute><BookDetails /></ProtectedRoute>} />
              <Route path="/borrowed" element={<Borrowed />} />
              <Route path="/fill-up-form" element={ <ProtectedRoute userOnly={true}><FillUpForm /></ProtectedRoute>} />
              <Route path="/dashboard" element={ <ProtectedRoute adminOnly={true}><Dashboard/></ProtectedRoute>} />
              <Route path="/upload" element={ <ProtectedRoute userOnly={true}><UploadBookPage /></ProtectedRoute>} />
              <Route path="/all-genres" element={<AllGenres />} />
              <Route path="/manage-books" element={ <ProtectedRoute adminOnly={true}><ManageBooks /></ProtectedRoute>} />
              <Route path="/manage-category" element={ <ProtectedRoute adminOnly={true}><ManageCategory /></ProtectedRoute>} />
              <Route path="/user" element={ <ProtectedRoute userOnly={true}><UserDashboard /></ProtectedRoute>} />
              <Route path="/loans" element={ <ProtectedRoute userOnly={true}><MyLoansBlank /></ProtectedRoute>} />
              {/* <Route path="/settings" element={ <ProtectedRoute userOnly={true}><UserSettings /></ProtectedRoute>} /> */}
              <Route path="/history" element={ <ProtectedRoute userOnly={true}><UserHistory /></ProtectedRoute>} />
              <Route path="/all-history" element={ <ProtectedRoute adminOnly={true}><AdminHistory /></ProtectedRoute>} />
              <Route path="/setting" element={ <ProtectedRoute adminOnly={true}><AdminSettings /></ProtectedRoute>} />
              <Route path="/manage-feature" element={ <ProtectedRoute adminOnly={true}><ManageFeature /></ProtectedRoute>} />
              <Route path="/donation-request" element={ <ProtectedRoute adminOnly={true}><DonationRequest /></ProtectedRoute>} />
              <Route path="/authgate" element={<AuthGate />} />
              <Route path="/calendar" element={<CalendarPage />} />
            </Route>
          )}
        </Routes>
      </main>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

