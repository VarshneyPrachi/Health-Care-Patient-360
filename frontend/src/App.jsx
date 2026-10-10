import { Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Patients from "./pages/Patients";
import Patient360 from "./pages/Patient360";
import Operations from "./pages/Operations";
import Financial from "./pages/Financial";
import AIRisk from "./pages/AIRisk";

function App() {
    return (
        <Routes>

            <Route element={<MainLayout />}>

                <Route
                    path="/"
                    element={<Dashboard />}
                />

                <Route
                    path="/patients"
                    element={<Patients />}
                />

                <Route
                    path="/patient-360"
                    element={<Patient360 />}
                />

                <Route
                    path="/operations"
                    element={<Operations />}
                />

                <Route
                    path="/financial"
                    element={<Financial />}
                />

                <Route
                    path="/ai-risk"
                    element={<AIRisk />}
                />

            </Route>

        </Routes>
    );
}

export default App;