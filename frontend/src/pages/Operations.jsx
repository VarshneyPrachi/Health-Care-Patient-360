import { useEffect, useState } from "react";

import {
    Activity,
    Building2,
    Clock3,
    AlertTriangle,
    Stethoscope,
    FlaskConical,
} from "lucide-react";

import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

import api from "../services/api";

function Operations() {
    const [departments, setDepartments] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [labs, setLabs] = useState([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadOperations = async () => {
            try {
                const [
                    departmentResponse,
                    doctorResponse,
                    labResponse,
                ] = await Promise.all([
                    api.get("/operations/departments"),
                    api.get("/operations/doctors"),
                    api.get("/operations/labs"),
                ]);

                setDepartments(
                    departmentResponse.data.data || []
                );

                setDoctors(
                    doctorResponse.data.data || []
                );

                setLabs(
                    labResponse.data.data || []
                );

            } catch (error) {
                console.error(
                    "Operations loading error:",
                    error
                );
            } finally {
                setLoading(false);
            }
        };

        loadOperations();
    }, []);


    const totalAdmissions = departments.reduce(
        (sum, item) =>
            sum + Number(item.admissions || 0),
        0
    );

    const totalEmergency = departments.reduce(
        (sum, item) =>
            sum + Number(item.emergency_admissions || 0),
        0
    );

    const averageLOS =
        departments.length > 0
            ? departments.reduce(
                  (sum, item) =>
                      sum + Number(item.average_los || 0),
                  0
              ) / departments.length
            : 0;


    const topDepartments = [...departments]
        .sort(
            (a, b) =>
                Number(b.admissions) -
                Number(a.admissions)
        )
        .slice(0, 8);


    const topLOS = [...departments]
        .sort(
            (a, b) =>
                Number(b.average_los) -
                Number(a.average_los)
        )
        .slice(0, 8);


    const topEmergency = [...departments]
        .sort(
            (a, b) =>
                Number(b.emergency_admissions) -
                Number(a.emergency_admissions)
        )
        .slice(0, 8);


    const topDoctors = [...doctors]
        .sort(
            (a, b) =>
                Number(b.admissions) -
                Number(a.admissions)
        )
        .slice(0, 8);


    const topLabs = [...labs]
        .sort(
            (a, b) =>
                Number(b.abnormal_tests) -
                Number(a.abnormal_tests)
        )
        .slice(0, 8);


    const kpis = [
        {
            title: "Departments",
            value: loading
                ? "..."
                : departments.length,
            subtitle: "Active departments",
            icon: Building2,
            className: "blue",
        },
        {
            title: "Admissions",
            value: loading
                ? "..."
                : totalAdmissions.toLocaleString("en-IN"),
            subtitle: "Tracked admissions",
            icon: Activity,
            className: "purple",
        },
        {
            title: "Average LOS",
            value: loading
                ? "..."
                : `${averageLOS.toFixed(2)} days`,
            subtitle: "Average length of stay",
            icon: Clock3,
            className: "green",
        },
        {
            title: "Emergency",
            value: loading
                ? "..."
                : totalEmergency.toLocaleString("en-IN"),
            subtitle: "Emergency admissions",
            icon: AlertTriangle,
            className: "orange",
        },
    ];


    return (
        <div>

            {/* Header */}

            <div className="operations-header">

                <div>
                    <div className="page-label">
                        CLINICAL OPERATIONS
                    </div>

                    <h1 className="page-title">
                        Operations & Clinical
                    </h1>

                    <p className="page-description">
                        Monitor departments, doctors,
                        admissions and laboratory activity.
                    </p>
                </div>

                <div className="operations-live">
                    <span />
                    Live Operations
                </div>

            </div>


            {/* KPI cards */}

            <div className="operations-kpi-grid">

                {kpis.map((item) => {
                    const Icon = item.icon;

                    return (
                        <div
                            className="operations-kpi"
                            key={item.title}
                        >

                            <div
                                className={`operations-kpi-icon ${item.className}`}
                            >
                                <Icon size={18} />
                            </div>

                            <div>

                                <div className="operations-kpi-value">
                                    {item.value}
                                </div>

                                <div className="operations-kpi-title">
                                    {item.title}
                                </div>

                                <div className="operations-kpi-subtitle">
                                    {item.subtitle}
                                </div>

                            </div>

                        </div>
                    );
                })}

            </div>


            {/* Charts row 1 */}

            <div className="operations-chart-grid">

                <div className="operations-card">

                    <div className="operations-card-header">

                        <div>
                            <div className="operations-card-title">
                                Department Admissions
                            </div>

                            <div className="operations-card-subtitle">
                                Patient activity by department
                            </div>
                        </div>

                        <div className="operations-card-icon blue">
                            <Building2 size={16} />
                        </div>

                    </div>

                    <div className="operations-chart">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >

                            <BarChart
                                data={topDepartments}
                                layout="vertical"
                                margin={{
                                    left: 10,
                                    right: 20,
                                    top: 5,
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
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#8994a7",
                                    }}
                                />

                                <YAxis
                                    type="category"
                                    dataKey="department_name"
                                    width={105}
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#69758a",
                                    }}
                                />

                                <Tooltip
                                    contentStyle={{
                                        border:
                                            "1px solid #e7ebf1",
                                        borderRadius:
                                            "9px",
                                        fontSize:
                                            "10px",
                                    }}
                                />

                                <Bar
                                    dataKey="admissions"
                                    fill="#0ea5e9"
                                    radius={[
                                        0,
                                        5,
                                        5,
                                        0,
                                    ]}
                                    barSize={15}
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </div>

                </div>


                <div className="operations-card">

                    <div className="operations-card-header">

                        <div>
                            <div className="operations-card-title">
                                Average Length of Stay
                            </div>

                            <div className="operations-card-subtitle">
                                Average patient stay by department
                            </div>
                        </div>

                        <div className="operations-card-icon green">
                            <Clock3 size={16} />
                        </div>

                    </div>

                    <div className="operations-chart">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >

                            <BarChart
                                data={topLOS}
                                layout="vertical"
                                margin={{
                                    left: 10,
                                    right: 20,
                                    top: 5,
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
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#8994a7",
                                    }}
                                />

                                <YAxis
                                    type="category"
                                    dataKey="department_name"
                                    width={105}
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#69758a",
                                    }}
                                />

                                <Tooltip
                                    formatter={(value) => [
                                        `${value} days`,
                                        "Average LOS",
                                    ]}
                                    contentStyle={{
                                        border:
                                            "1px solid #e7ebf1",
                                        borderRadius:
                                            "9px",
                                        fontSize:
                                            "10px",
                                    }}
                                />

                                <Bar
                                    dataKey="average_los"
                                    fill="#22c55e"
                                    radius={[
                                        0,
                                        5,
                                        5,
                                        0,
                                    ]}
                                    barSize={15}
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </div>

                </div>

            </div>


            {/* Charts row 2 */}

            <div className="operations-chart-grid">

                <div className="operations-card">

                    <div className="operations-card-header">

                        <div>
                            <div className="operations-card-title">
                                Emergency Admissions
                            </div>

                            <div className="operations-card-subtitle">
                                Emergency activity by department
                            </div>
                        </div>

                        <div className="operations-card-icon orange">
                            <AlertTriangle size={16} />
                        </div>

                    </div>

                    <div className="operations-chart">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >

                            <BarChart
                                data={topEmergency}
                                layout="vertical"
                                margin={{
                                    left: 10,
                                    right: 20,
                                    top: 5,
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
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#8994a7",
                                    }}
                                />

                                <YAxis
                                    type="category"
                                    dataKey="department_name"
                                    width={105}
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#69758a",
                                    }}
                                />

                                <Tooltip
                                    contentStyle={{
                                        border:
                                            "1px solid #e7ebf1",
                                        borderRadius:
                                            "9px",
                                        fontSize:
                                            "10px",
                                    }}
                                />

                                <Bar
                                    dataKey="emergency_admissions"
                                    fill="#f59e0b"
                                    radius={[
                                        0,
                                        5,
                                        5,
                                        0,
                                    ]}
                                    barSize={15}
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </div>

                </div>


                <div className="operations-card">

                    <div className="operations-card-header">

                        <div>
                            <div className="operations-card-title">
                                Doctor Workload
                            </div>

                            <div className="operations-card-subtitle">
                                Admissions handled by doctors
                            </div>
                        </div>

                        <div className="operations-card-icon purple">
                            <Stethoscope size={16} />
                        </div>

                    </div>

                    <div className="operations-chart">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >

                            <BarChart
                                data={topDoctors}
                                layout="vertical"
                                margin={{
                                    left: 10,
                                    right: 20,
                                    top: 5,
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
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#8994a7",
                                    }}
                                />

                                <YAxis
                                    type="category"
                                    dataKey="doctor_name"
                                    width={125}
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 7,
                                        fill: "#69758a",
                                    }}
                                />

                                <Tooltip
                                    contentStyle={{
                                        border:
                                            "1px solid #e7ebf1",
                                        borderRadius:
                                            "9px",
                                        fontSize:
                                            "10px",
                                    }}
                                />

                                <Bar
                                    dataKey="admissions"
                                    fill="#8b5cf6"
                                    radius={[
                                        0,
                                        5,
                                        5,
                                        0,
                                    ]}
                                    barSize={15}
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </div>

                </div>

            </div>


            {/* Laboratory */}

            <div className="operations-card laboratory-card">

                <div className="operations-card-header">

                    <div>
                        <div className="operations-card-title">
                            Laboratory Intelligence
                        </div>

                        <div className="operations-card-subtitle">
                            Tests with the highest number of abnormal results
                        </div>
                    </div>

                    <div className="operations-card-icon red">
                        <FlaskConical size={16} />
                    </div>

                </div>


                <div className="lab-grid">

                    {topLabs.map((lab) => {

                        const abnormal =
                            Number(
                                lab.abnormal_tests || 0
                            );

                        const total =
                            Number(
                                lab.total_tests || 0
                            );

                        const percentage =
                            total > 0
                                ? (abnormal / total) * 100
                                : 0;

                        return (
                            <div
                                className="lab-item"
                                key={lab.test_name}
                            >

                                <div className="lab-top">

                                    <span>
                                        {lab.test_name}
                                    </span>

                                    <strong>
                                        {abnormal}
                                    </strong>

                                </div>

                                <div className="lab-bar">

                                    <div
                                        style={{
                                            width: `${Math.min(
                                                percentage,
                                                100
                                            )}%`,
                                        }}
                                    />

                                </div>

                                <div className="lab-bottom">
                                    {total.toLocaleString("en-IN")} total tests
                                    <span>
                                        {percentage.toFixed(1)}% abnormal
                                    </span>
                                </div>

                            </div>
                        );
                    })}

                </div>

            </div>


            <div className="demo-note">
                <strong>Analytics note:</strong>{" "}
                Operational metrics are based on the project's
                healthcare dataset and are intended for analytical
                demonstration.
            </div>

        </div>
    );
}

export default Operations;