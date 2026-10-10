import { useEffect, useState } from "react";
import {
    Activity,
    Users,
    IndianRupee,
    Clock3,
    ArrowUpRight,
    BrainCircuit,
    Building2,
} from "lucide-react";

import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    PieChart,
    Pie,
    Cell,
} from "recharts";

import api from "../services/api";

function Dashboard() {
    const [summary, setSummary] = useState(null);
    const [riskData, setRiskData] = useState([]);
    const [departmentData, setDepartmentData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                const [
                    summaryResponse,
                    riskResponse,
                    departmentResponse,
                ] = await Promise.all([
                    api.get("/dashboard/summary"),
                    api.get("/ai/risk-distribution"),
                    api.get("/operations/departments"),
                ]);

                setSummary(summaryResponse.data.data);

                setRiskData(
                    riskResponse.data.data.map((item) => ({
                        name: item.risk_category,
                        value: Number(item.patient_count),
                    }))
                );

                setDepartmentData(
                    departmentResponse.data.data
                        .slice(0, 6)
                        .map((item) => ({
                            name: item.department_name,
                            admissions: Number(item.admissions),
                        }))
                );

            } catch (error) {
                console.error(
                    "Dashboard loading error:",
                    error
                );
            } finally {
                setLoading(false);
            }
        };

        loadDashboard();
    }, []);

    const formatRevenue = (value) => {
        if (!value) return "₹0";

        const revenue = Number(value);

        if (revenue >= 1000000000) {
            return `₹${(revenue / 1000000000).toFixed(2)}B`;
        }

        if (revenue >= 1000000) {
            return `₹${(revenue / 1000000).toFixed(1)}M`;
        }

        return `₹${revenue.toLocaleString("en-IN")}`;
    };

    const stats = [
        {
            title: "Total Patients",
            value: loading
                ? "..."
                : Number(summary?.patients || 0).toLocaleString("en-IN"),
            icon: Users,
            description: "Unique patients",
        },
        {
            title: "Admissions",
            value: loading
                ? "..."
                : Number(summary?.admissions || 0).toLocaleString("en-IN"),
            icon: Activity,
            description: "Hospital admissions",
        },
        {
            title: "Total Revenue",
            value: loading
                ? "..."
                : formatRevenue(summary?.total_revenue),
            icon: IndianRupee,
            description: "Recorded hospital revenue",
        },
        {
            title: "Average Stay",
            value: loading
                ? "..."
                : `${summary?.average_los || 0}`,
            icon: Clock3,
            description: "Average length of stay",
        },
    ];

    const riskColors = {
        High: "#ef4444",
        Medium: "#f59e0b",
        Low: "#22c55e",
    };

    return (
        <div>

            {/* Header */}

            <div className="dashboard-header">

                <div>
                    <div className="page-label">
                        HOSPITAL INTELLIGENCE
                    </div>

                    <h1 className="page-title">
                        Hospital Overview
                    </h1>

                    <p className="page-description">
                        A unified view of patients, admissions,
                        operations and AI-powered healthcare insights.
                    </p>
                </div>

                <div className="dashboard-status">
                    <span></span>
                    Live Data
                </div>

            </div>


            {/* KPI Cards */}

            <div className="stats-grid">

                {stats.map((stat) => {
                    const Icon = stat.icon;

                    return (
                        <div
                            className="stat-card"
                            key={stat.title}
                        >

                            <div className="stat-top">

                                <div className="stat-icon">
                                    <Icon size={19} />
                                </div>

                                <ArrowUpRight
                                    size={15}
                                    className="stat-arrow"
                                />

                            </div>

                            <div className="stat-value">
                                {stat.value}
                            </div>

                            <div className="stat-title">
                                {stat.title}
                            </div>

                            <div className="stat-description">
                                {stat.description}
                            </div>

                        </div>
                    );
                })}

            </div>


            {/* Main Charts */}

            <div className="dashboard-chart-grid">

                {/* Department admissions */}

                <div className="analytics-card department-chart-card">

                    <div className="card-header">

                        <div>
                            <div className="card-title">
                                Department Activity
                            </div>

                            <div className="card-subtitle">
                                Admissions across major departments
                            </div>
                        </div>

                        <div className="card-icon-small">
                            <Building2 size={16} />
                        </div>

                    </div>

                    <div className="chart-container">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >
                            <BarChart
                                data={departmentData}
                                layout="vertical"
                                margin={{
                                    top: 5,
                                    right: 20,
                                    left: 20,
                                    bottom: 5,
                                }}
                            >

                                <CartesianGrid
                                    strokeDasharray="3 3"
                                    horizontal={false}
                                    stroke="#edf0f4"
                                />

                                <XAxis
                                    type="number"
                                    tick={{
                                        fontSize: 9,
                                        fill: "#8994a7",
                                    }}
                                    axisLine={false}
                                    tickLine={false}
                                />

                                <YAxis
                                    dataKey="name"
                                    type="category"
                                    width={100}
                                    tick={{
                                        fontSize: 9,
                                        fill: "#65728a",
                                    }}
                                    axisLine={false}
                                    tickLine={false}
                                />

                                <Tooltip
                                    cursor={{
                                        fill: "#f6f8fb",
                                    }}
                                    contentStyle={{
                                        border: "1px solid #e7ebf1",
                                        borderRadius: "10px",
                                        fontSize: "11px",
                                    }}
                                />

                                <Bar
                                    dataKey="admissions"
                                    fill="#0ea5e9"
                                    radius={[0, 6, 6, 0]}
                                    barSize={17}
                                />

                            </BarChart>
                        </ResponsiveContainer>

                    </div>

                </div>


                {/* Risk */}

                <div className="analytics-card">

                    <div className="card-header">

                        <div>
                            <div className="card-title">
                                Patient Risk
                            </div>

                            <div className="card-subtitle">
                                AI risk distribution
                            </div>
                        </div>

                        <div className="card-icon-small ai">
                            <BrainCircuit size={16} />
                        </div>

                    </div>

                    <div className="risk-chart-wrapper">

                        <ResponsiveContainer
                            width="55%"
                            height="100%"
                        >
                            <PieChart>

                                <Pie
                                    data={riskData}
                                    dataKey="value"
                                    nameKey="name"
                                    innerRadius={55}
                                    outerRadius={78}
                                    paddingAngle={3}
                                    stroke="none"
                                >

                                    {riskData.map(
                                        (entry) => (
                                            <Cell
                                                key={entry.name}
                                                fill={
                                                    riskColors[
                                                        entry.name
                                                    ] || "#94a3b8"
                                                }
                                            />
                                        )
                                    )}

                                </Pie>

                                <Tooltip />

                            </PieChart>
                        </ResponsiveContainer>


                        <div className="risk-list">

                            {riskData.map((item) => (
                                <div
                                    className="risk-item"
                                    key={item.name}
                                >

                                    <div className="risk-name">

                                        <span
                                            className="risk-dot"
                                            style={{
                                                background:
                                                    riskColors[
                                                        item.name
                                                    ],
                                            }}
                                        />

                                        {item.name}

                                    </div>

                                    <strong>
                                        {item.value.toLocaleString(
                                            "en-IN"
                                        )}
                                    </strong>

                                </div>
                            ))}

                        </div>

                    </div>

                </div>

            </div>


            {/* Intelligence Cards */}

            <div className="insight-grid">

                <div className="insight-card ai-insight">

                    <div className="insight-icon">
                        <BrainCircuit size={20} />
                    </div>

                    <div className="insight-content">

                        <div className="insight-label">
                            AI PATIENT INTELLIGENCE
                        </div>

                        <div className="insight-title">
                            Predictive healthcare analytics
                        </div>

                        <div className="insight-text">
                            Explore readmission risk and predicted
                            length of stay generated by the project's
                            machine-learning models.
                        </div>

                    </div>

                    <ArrowUpRight size={18} />

                </div>


                <div className="mini-card">

                    <div className="mini-label">
                        AI Risk Engine
                    </div>

                    <div className="mini-value">
                        Active
                    </div>

                    <div className="mini-status">
                        <span></span>
                        Model available
                    </div>

                </div>


                <div className="mini-card">

                    <div className="mini-label">
                        Data Coverage
                    </div>

                    <div className="mini-value">
                        5K+
                    </div>

                    <div className="mini-status">
                        <span></span>
                        Patient records
                    </div>

                </div>

            </div>


            <div className="demo-note">
                <strong>Analytics note:</strong>{" "}
                AI predictions are based on the project's synthetic
                healthcare dataset and are intended for analytical
                demonstration, not clinical diagnosis.
            </div>

        </div>
    );
}

export default Dashboard;