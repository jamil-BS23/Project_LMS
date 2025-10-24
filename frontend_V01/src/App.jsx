// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
// import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
// import Home from './pages/Home/Home';
// import Navbar from './components/Navbar/Navbar';
// import BookDetails from './pages/BookDetails/BookDetails';
// import Layout from './components/Layout/Layout';
// import Borrowed from './pages/Borrowed/Borrowed';
// import FillUpForm from './components/FillUpForm/FillUpForm';
// import Dashboard from './pages/Dashboad/Dashboad';
// import UploadBookPage from './components/Upload/UploadBookPage';
// import AllGenres from './pages/AllGenres/AllGenres';
// import ManageBooks from './pages/ManageBooks/ManageBooks';
// import ManageCategory from './pages/ManageCategory/ManageCategory';
// import UserDashboard from './pages/User/UserDashboard';
// import MyLoansBlank from './pages/MyLoansBlank/MyLoansBlank';
// import UserSettings from './pages/UserSettings/UserSettings';
// import UserHistory from './pages/UserHistory/UserHistory';
// import AdminSettings from './pages/AdminSettings/AdminSettings';
// import AdminHistory  from './pages/AdminSettings/AdminHistory';
// import ManageFeature from './pages/ManageFeature/ManageFeature';
// import DonationRequest from './pages/DonationRequest/DonationRequest';
// import { AuthProvider } from './Providers/AuthProvider';
// import AuthGate from './pages/AuthGate/AuthGate';
// import CalendarPage from './pages/Calendar/CalendarPage';
// import Login from './pages/Auth/Login';

// function App() {
  
//   return (
//     <BrowserRouter>
//     < Navbar />
//           <main className="flex-grow">
//       <Routes>
//                 <Route element={<Layout />}>
//         <Route path="/" element={<Home />} />
//                   <Route path="/book/:id" element={<BookDetails />} /> {/* <-- ADD THE NEW ROUTE */}
//                   <Route path="/borrowed" element={<Borrowed />} />
//                   <Route path="/fill-up-form" element={<FillUpForm />} />
//                   <Route path="/dashboard" element={<Dashboard />} />
//                   <Route path="/upload" element={<UploadBookPage />} />
//                   <Route path="/all-genres" element={<AllGenres />} />
//                           <Route path="/manage-books" element={<ManageBooks />} />
//                                   <Route path="/manage-category" element={<ManageCategory />} />
//                     <Route path="/user" element={<UserDashboard />} />
//                     <Route path="/loans" element={<MyLoansBlank/>} />
//                     <Route path="/settings" element={<UserSettings/>} />
//                     <Route path="/history" element={<UserHistory/>} />
//                     <Route path="/all-history" element={<AdminHistory/>} />
//                     <Route path="/setting" element={<AdminSettings/>} />
//                     <Route path="/manage-feature" element={<ManageFeature />} />
//                     <Route path="/donation-request" element={<DonationRequest />} />
//                                         <Route path="/authgate" element={<AuthGate />} />
// <Route path="/calendar" element={<CalendarPage />} />
// <Route path="/login" element={<Login />} /> 



                    

//                           </Route>
//       </Routes>
//             </main>
//     </BrowserRouter>
//   );
// }

// export default App;

// // App.jsx
// import "./App.css";
// import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

// import Navbar from "./components/Navbar/Navbar";
// import Layout from "./components/Layout/Layout";

// import Home from "./pages/Home/Home";
// import BookDetails from "./pages/BookDetails/BookDetails";
// import Borrowed from "./pages/Borrowed/Borrowed";
// import FillUpForm from "./components/FillUpForm/FillUpForm";
// import Dashboard from "./pages/Dashboad/Dashboad";
// import UploadBookPage from "./components/Upload/UploadBookPage";
// import AllGenres from "./pages/AllGenres/AllGenres";
// import ManageBooks from "./pages/ManageBooks/ManageBooks";
// import ManageCategory from "./pages/ManageCategory/ManageCategory";

// function App() {
//   return (
//     <BrowserRouter>
//       <Navbar />
//       <main className="flex-grow">
//         <Routes>
//           {/* Wrap everything with your Layout */}
//           <Route element={<Layout />}>
//             {/* Canonical routes */}
//             <Route path="/" element={<Home />} />
//             <Route path="/book/:id" element={<BookDetails />} />
//             <Route path="/borrowed" element={<Borrowed />} />
//             <Route path="/fill-up-form" element={<FillUpForm />} />
//             <Route path="/dashboard" element={<Dashboard />} />
//             <Route path="/upload" element={<UploadBookPage />} />
//             <Route path="/all-genres" element={<AllGenres />} />
//             <Route path="/manage-books" element={<ManageBooks />} />
//             <Route path="/manage-category" element={<ManageCategory />} />

//             {/* ---- QUICK ALIASES so /admin/* also works ---- */}
//             <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
//             <Route path="/admin/dashboard" element={<Dashboard />} />
//             <Route path="/admin/borrowed" element={<Borrowed />} />
//             <Route path="/admin/fill-up-form" element={<FillUpForm />} />
//             <Route path="/admin/upload" element={<UploadBookPage />} />
//             <Route path="/admin/all-genres" element={<AllGenres />} />
//             <Route path="/admin/manage-books" element={<ManageBooks />} />
//             <Route path="/admin/manage-category" element={<ManageCategory />} />

//             {/* Fallbacks */}
//             <Route path="*" element={<Navigate to="/dashboard" replace />} />
//           </Route>
//         </Routes>
//       </main>
//     </BrowserRouter>
//   );
// }

// export default App;



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
              <Route path="/settings" element={ <ProtectedRoute userOnly={true}><UserSettings /></ProtectedRoute>} />
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

