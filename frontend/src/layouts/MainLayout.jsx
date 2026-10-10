import {
    Activity,
    BrainCircuit,
    LayoutDashboard,
    UserRound,
    Users,
    WalletCards,
    Bell,
    Search,
    ChevronDown,
    Menu,
    X,
} from "lucide-react";

import { NavLink, Outlet } from "react-router-dom";
import { useState } from "react";

function MainLayout() {
    const [mobileOpen, setMobileOpen] = useState(false);

    const navigation = [
        {
            name: "Overview",
            path: "/",
            icon: LayoutDashboard,
        },
        {
            name: "Patients",
            path: "/patients",
            icon: Users,
        },
        {
            name: "Patient 360",
            path: "/patient-360",
            icon: UserRound,
        },
        {
            name: "Operations",
            path: "/operations",
            icon: Activity,
        },
        {
            name: "Financial",
            path: "/financial",
            icon: WalletCards,
        },
        {
            name: "AI Risk",
            path: "/ai-risk",
            icon: BrainCircuit,
        },
    ];

    return (
        <div className="app-shell">

            {mobileOpen && (
                <div
                    className="mobile-overlay"
                    onClick={() => setMobileOpen(false)}
                />
            )}

            <aside
                className={`sidebar ${
                    mobileOpen ? "sidebar-open" : ""
                }`}
            >

                <div className="brand">

                    <div className="brand-icon">
                        <Activity size={21} />
                    </div>

                    <div className="brand-copy">
                        <div className="brand-title">
                            Patient 360
                        </div>

                        <div className="brand-subtitle">
                            Healthcare Intelligence
                        </div>
                    </div>

                    <button
                        className="mobile-close"
                        onClick={() => setMobileOpen(false)}
                    >
                        <X size={20} />
                    </button>

                </div>


                <div className="nav-section-title">
                    MAIN MENU
                </div>

                <nav className="sidebar-nav">

                    {navigation.map((item) => {
                        const Icon = item.icon;

                        return (
                            <NavLink
                                key={item.name}
                                to={item.path}
                                end={item.path === "/"}
                                onClick={() =>
                                    setMobileOpen(false)
                                }
                                className={({ isActive }) =>
                                    `nav-item ${
                                        isActive ? "active" : ""
                                    }`
                                }
                            >
                                <Icon size={18} />
                                <span>{item.name}</span>
                            </NavLink>
                        );
                    })}

                </nav>


                <div className="sidebar-bottom">

                    <div className="system-status">

                        <div className="status-dot" />

                        <div>
                            <div className="status-title">
                                System Online
                            </div>

                            <div className="status-text">
                                All services operational
                            </div>
                        </div>

                    </div>

                    <div className="sidebar-version">
                        Healthcare Patient 360 · v1.0
                    </div>

                </div>

            </aside>


            <div className="main-area">

                <header className="topbar">

                    <div className="topbar-left">

                        <button
                            className="mobile-menu"
                            onClick={() =>
                                setMobileOpen(true)
                            }
                        >
                            <Menu size={21} />
                        </button>

                        <div className="search-box">

                            <Search size={17} />

                            <input
                                type="text"
                                placeholder="Search patients, departments..."
                            />

                            <span className="search-shortcut">
                                Ctrl K
                            </span>

                        </div>

                    </div>


                    <div className="topbar-right">

                        <button className="icon-button">
                            <Bell size={18} />
                            <span className="notification-dot" />
                        </button>


                        <div className="profile">

                            <div className="avatar">
                                A
                            </div>

                            <div className="profile-info">

                                <div className="profile-name">
                                    Administrator
                                </div>

                                <div className="profile-role">
                                    Hospital Analytics
                                </div>

                            </div>

                            <ChevronDown size={15} />

                        </div>

                    </div>

                </header>


                <main className="content">
                    <Outlet />
                </main>

            </div>

        </div>
    );
}

export default MainLayout;