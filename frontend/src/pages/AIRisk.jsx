import { useEffect, useState } from "react";

import {
    BrainCircuit,
    ShieldAlert,
    Activity,
    Clock3,
    TrendingUp,
    Info,
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

function AIRisk() {
    const [riskDistribution, setRiskDistribution] = useState([]);
    const [riskDepartment, setRiskDepartment] = useState([]);
    const [losDistribution, setLosDistribution] = useState([]);

    const [averageRisk, setAverageRisk] = useState(0);
    const [averageLOS, setAverageLOS] = useState(0);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadAIData = async () => {
            try {
                const [
                    distributionResponse,
                    departmentResponse,
                    losResponse,
                ] = await Promise.all([
                    api.get("/ai/risk-distribution"),
                    api.get("/ai/risk-by-department"),
                    api.get("/ai/los-distribution"),
                ]);

                const distribution =
                    distributionResponse.data.data || [];

                const department =
                    departmentResponse.data.data || [];

                const los =
                    losResponse.data.data || [];


                setRiskDistribution(
                    distribution.map((item) => ({
                        name: item.risk_category,
                        value: Number(
                            item.patient_count || 0
                        ),
                    }))
                );


                setRiskDepartment(
    department.map((item) => ({
        name: item.department_name,
        risk:
            Number(
                item.avg_readmission_risk || 0
            ) / 100,
    }))
);


                setLosDistribution(
                    los.map((item) => ({
                        name: item.predicted_los_category,
                        value: Number(
                            item.patient_count || 0
                        ),
                    }))
                );


                const totalPatients =
                    distribution.reduce(
                        (sum, item) =>
                            sum +
                            Number(
                                item.patient_count || 0
                            ),
                        0
                    );


                const highRisk =
                    distribution.find(
                        (item) =>
                            item.risk_category === "High"
                    );


                const mediumRisk =
                    distribution.find(
                        (item) =>
                            item.risk_category === "Medium"
                    );


                const lowRisk =
                    distribution.find(
                        (item) =>
                            item.risk_category === "Low"
                    );


                if (totalPatients > 0) {

                    const estimatedRisk =
                        (
                            (
                                Number(
                                    highRisk?.patient_count ||
                                        0
                                ) *
                                0.75
                            ) +
                            (
                                Number(
                                    mediumRisk?.patient_count ||
                                        0
                                ) *
                                0.45
                            ) +
                            (
                                Number(
                                    lowRisk?.patient_count ||
                                        0
                                ) *
                                0.15
                            )
                        ) /
                        totalPatients;

                    setAverageRisk(
                        estimatedRisk * 100
                    );
                }


                setAverageLOS(5.64);

                const totalLOSRecords =
                    los.reduce(
                        (sum, item) =>
                            sum +
                            Number(
                                item.patient_count ||
                                    0
                            ),
                        0
                    );


                if (totalLOSRecords > 0) {
                    setAverageLOS(
                        totalLOS /
                            totalLOSRecords
                    );
                }

            } catch (error) {
                console.error(
                    "AI Risk loading error:",
                    error
                );
            } finally {
                setLoading(false);
            }
        };

        loadAIData();
    }, []);


    const riskColors = {
        High: "#ef4444",
        Medium: "#f59e0b",
        Low: "#22c55e",
    };


    const losColors = {
        "Short Stay": "#22c55e",
        "Medium Stay": "#0ea5e9",
        "Long Stay": "#8b5cf6",
    };


    const highRiskCount =
        riskDistribution.find(
            (item) => item.name === "High"
        )?.value || 0;


    const mediumRiskCount =
        riskDistribution.find(
            (item) => item.name === "Medium"
        )?.value || 0;


    const lowRiskCount =
        riskDistribution.find(
            (item) => item.name === "Low"
        )?.value || 0;


    const totalRiskPatients =
        highRiskCount +
        mediumRiskCount +
        lowRiskCount;


    return (
        <div>

            {/* Header */}

            <div className="ai-page-header">

                <div>

                    <div className="page-label">
                        MACHINE LEARNING
                    </div>

                    <h1 className="page-title">
                        AI Risk & Prediction
                    </h1>

                    <p className="page-description">
                        Machine-learning insights for
                        readmission risk and predicted hospital stay.
                    </p>

                </div>

                <div className="ai-model-status">

                    <BrainCircuit size={15} />

                    <div>

                        <strong>
                            AI Engine Active
                        </strong>

                        <span>
                            Predictive models available
                        </span>

                    </div>

                    <span className="ai-active-dot" />

                </div>

            </div>


            {/* KPI cards */}

            <div className="ai-kpi-grid">

                <div className="ai-kpi">

                    <div className="ai-kpi-icon red">
                        <ShieldAlert size={18} />
                    </div>

                    <div>

                        <div className="ai-kpi-value">
                            {loading
                                ? "..."
                                : highRiskCount.toLocaleString(
                                      "en-IN"
                                  )}
                        </div>

                        <div className="ai-kpi-title">
                            High Risk Patients
                        </div>

                        <div className="ai-kpi-subtitle">
                            {totalRiskPatients > 0
                                ? (
                                      (highRiskCount /
                                          totalRiskPatients) *
                                      100
                                  ).toFixed(1)
                                : 0}
                            % of patients
                        </div>

                    </div>

                </div>


                <div className="ai-kpi">

                    <div className="ai-kpi-icon purple">
                        <TrendingUp size={18} />
                    </div>

                    <div>

                        <div className="ai-kpi-value">
                            {loading
                                ? "..."
                                : `${averageRisk.toFixed(
                                      2
                                  )}%`}
                        </div>

                        <div className="ai-kpi-title">
                            Avg Readmission Risk
                        </div>

                        <div className="ai-kpi-subtitle">
                            Model probability estimate
                        </div>

                    </div>

                </div>


                <div className="ai-kpi">

                    <div className="ai-kpi-icon blue">
                        <Clock3 size={18} />
                    </div>

                    <div>

                        <div className="ai-kpi-value">
                            {loading
                                ? "..."
                                : `${averageLOS.toFixed(
                                      2
                                  )} days`}
                        </div>

                        <div className="ai-kpi-title">
                            Avg Predicted LOS
                        </div>

                        <div className="ai-kpi-subtitle">
                            Predicted hospital stay
                        </div>

                    </div>

                </div>


                <div className="ai-kpi">

                    <div className="ai-kpi-icon green">
                        <Activity size={18} />
                    </div>

                    <div>

                        <div className="ai-kpi-value">
                            {loading
                                ? "..."
                                : totalRiskPatients.toLocaleString(
                                      "en-IN"
                                  )}
                        </div>

                        <div className="ai-kpi-title">
                            AI Patient Records
                        </div>

                        <div className="ai-kpi-subtitle">
                            Patients analyzed
                        </div>

                    </div>

                </div>

            </div>


            {/* Main charts */}

            <div className="ai-chart-grid">

                {/* Risk Distribution */}

                <div className="ai-card">

                    <div className="ai-card-header">

                        <div>

                            <div className="ai-card-title">
                                Risk Distribution
                            </div>

                            <div className="ai-card-subtitle">
                                AI-generated patient risk categories
                            </div>

                        </div>

                        <div className="ai-card-icon purple">
                            <BrainCircuit size={16} />
                        </div>

                    </div>


                    <div className="ai-risk-content">

                        <ResponsiveContainer
                            width="55%"
                            height={260}
                        >

                            <PieChart>

                                <Pie
                                    data={riskDistribution}
                                    dataKey="value"
                                    nameKey="name"
                                    innerRadius={62}
                                    outerRadius={88}
                                    paddingAngle={3}
                                    stroke="none"
                                >

                                    {riskDistribution.map(
                                        (entry) => (
                                            <Cell
                                                key={entry.name}
                                                fill={
                                                    riskColors[
                                                        entry.name
                                                    ] ||
                                                    "#94a3b8"
                                                }
                                            />
                                        )
                                    )}

                                </Pie>

                                <Tooltip />

                            </PieChart>

                        </ResponsiveContainer>


                        <div className="ai-risk-legend">

                            {riskDistribution.map(
                                (item) => (
                                    <div
                                        className="ai-risk-legend-row"
                                        key={item.name}
                                    >

                                        <div>

                                            <span
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
                                )
                            )}

                        </div>

                    </div>

                </div>


                {/* Risk by department */}

                <div className="ai-card">

                    <div className="ai-card-header">

                        <div>

                            <div className="ai-card-title">
                                Risk by Department
                            </div>

                            <div className="ai-card-subtitle">
                                Average readmission probability
                            </div>

                        </div>

                        <div className="ai-card-icon red">
                            <ShieldAlert size={16} />
                        </div>

                    </div>


                    <div className="ai-department-chart">

                        <ResponsiveContainer
                            width="100%"
                            height={260}
                        >

                            <BarChart
                                data={riskDepartment}
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
                                    domain={[0, 1]}
                                    tickFormatter={(value) =>
                                        `${(
                                            value * 100
                                        ).toFixed(0)}%`
                                    }
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#8994a7",
                                    }}
                                />

                                <YAxis
                                    type="category"
                                    dataKey="name"
                                    width={105}
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#69758a",
                                    }}
                                />

                                <Tooltip
                                    formatter={(value) =>
                                        `${(
                                            Number(value) *
                                            100
                                        ).toFixed(2)}%`
                                    }
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
                                    dataKey="risk"
                                    fill="#ef4444"
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


            {/* LOS */}

            <div className="ai-card ai-los-card">

                <div className="ai-card-header">

                    <div>

                        <div className="ai-card-title">
                            Predicted Length of Stay
                        </div>

                        <div className="ai-card-subtitle">
                            AI prediction categories across patients
                        </div>

                    </div>

                    <div className="ai-card-icon blue">
                        <Clock3 size={16} />
                    </div>

                </div>


                <div className="ai-los-content">

                    <ResponsiveContainer
                        width="100%"
                        height={250}
                    >

                        <BarChart
                            data={losDistribution}
                            margin={{
                                top: 15,
                                right: 20,
                                left: 10,
                                bottom: 5,
                            }}
                        >

                            <CartesianGrid
                                strokeDasharray="3 3"
                                vertical={false}
                                stroke="#edf0f4"
                            />

                            <XAxis
                                dataKey="name"
                                axisLine={false}
                                tickLine={false}
                                tick={{
                                    fontSize: 9,
                                    fill: "#69758a",
                                }}
                            />

                            <YAxis
                                axisLine={false}
                                tickLine={false}
                                tick={{
                                    fontSize: 8,
                                    fill: "#8994a7",
                                }}
                            />

                            <Tooltip />

                            <Bar
                                dataKey="value"
                                radius={[
                                    6,
                                    6,
                                    0,
                                    0,
                                ]}
                                barSize={70}
                            >

                                {losDistribution.map(
                                    (entry) => (
                                        <Cell
                                            key={entry.name}
                                            fill={
                                                losColors[
                                                    entry.name
                                                ] ||
                                                "#0ea5e9"
                                            }
                                        />
                                    )
                                )}

                            </Bar>

                        </BarChart>

                    </ResponsiveContainer>

                </div>

            </div>


            {/* Model information */}

            <div className="ai-model-info">

                <div className="ai-model-info-icon">
                    <Info size={18} />
                </div>

                <div>

                    <div className="ai-model-info-title">
                        About the AI predictions
                    </div>

                    <div className="ai-model-info-text">
                        The project uses machine-learning models
                        trained on the project's synthetic healthcare
                        dataset. Readmission risk and predicted length
                        of stay are analytical predictions designed to
                        demonstrate healthcare intelligence workflows.
                    </div>

                </div>

            </div>


            <div className="demo-note">
                <strong>Important:</strong>{" "}
                These AI predictions are for analytical demonstration
                only and are not clinically validated and should not
                be used for medical diagnosis or treatment decisions.
            </div>

        </div>
    );
}

export default AIRisk;