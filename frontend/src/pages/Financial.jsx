import { useEffect, useState } from "react";

import {
    IndianRupee,
    ShieldCheck,
    CreditCard,
    Receipt,
    Building2,
    WalletCards,
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

function Financial() {
    const [summary, setSummary] = useState(null);
    const [insurance, setInsurance] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [paymentStatus, setPaymentStatus] = useState([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadFinancial = async () => {
            try {
                const [
                    summaryResponse,
                    insuranceResponse,
                    departmentResponse,
                    paymentResponse,
                ] = await Promise.all([
                    api.get("/financial/summary"),
                    api.get("/financial/by-insurance"),
                    api.get("/financial/by-department"),
                    api.get("/financial/payment-status"),
                ]);

                setSummary(
                    summaryResponse.data.data
                );

                setInsurance(
                    insuranceResponse.data.data || []
                );

                setDepartments(
                    departmentResponse.data.data || []
                );

                setPaymentStatus(
                    paymentResponse.data.data || []
                );

            } catch (error) {
                console.error(
                    "Financial loading error:",
                    error
                );
            } finally {
                setLoading(false);
            }
        };

        loadFinancial();
    }, []);


    const money = (value) => {
        const number = Number(value || 0);

        if (number >= 1000000000) {
            return `₹${(
                number / 1000000000
            ).toFixed(2)}B`;
        }

        if (number >= 1000000) {
            return `₹${(
                number / 1000000
            ).toFixed(1)}M`;
        }

        return `₹${number.toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 0,
            }
        )}`;
    };


    const revenueByDepartment = [...departments]
        .sort(
            (a, b) =>
                Number(b.total_revenue) -
                Number(a.total_revenue)
        )
        .slice(0, 8);


    const insuranceChart = insurance.map(
        (item) => ({
            name: item.insurance_type,
            revenue: Number(item.total_revenue || 0),
        })
    );


    const paymentChart = paymentStatus.map(
        (item) => ({
            name: item.payment_status,
            value: Number(item.count || 0),
        })
    );


    const paymentColors = [
        "#0ea5e9",
        "#22c55e",
        "#f59e0b",
        "#8b5cf6",
        "#ef4444",
    ];


    const cards = [
        {
            title: "Total Revenue",
            value: loading
                ? "..."
                : money(summary?.total_revenue),
            subtitle: "Recorded hospital revenue",
            icon: IndianRupee,
            className: "blue",
        },
        {
            title: "Insurance Covered",
            value: loading
                ? "..."
                : money(summary?.insurance_covered),
            subtitle: "Insurance contribution",
            icon: ShieldCheck,
            className: "green",
        },
        {
            title: "Patient Paid",
            value: loading
                ? "..."
                : money(summary?.patient_paid),
            subtitle: "Patient contribution",
            icon: CreditCard,
            className: "purple",
        },
        {
            title: "Average Bill",
            value: loading
                ? "..."
                : money(summary?.average_bill),
            subtitle: "Average admission bill",
            icon: Receipt,
            className: "orange",
        },
    ];


    return (
        <div>

            {/* Header */}

            <div className="financial-header">

                <div>

                    <div className="page-label">
                        FINANCIAL INTELLIGENCE
                    </div>

                    <h1 className="page-title">
                        Financial Intelligence
                    </h1>

                    <p className="page-description">
                        Monitor hospital revenue,
                        insurance coverage and patient payments.
                    </p>

                </div>

                <div className="financial-live">
                    <span />
                    Financial Data
                </div>

            </div>


            {/* KPI cards */}

            <div className="financial-kpi-grid">

                {cards.map((card) => {
                    const Icon = card.icon;

                    return (
                        <div
                            className="financial-kpi"
                            key={card.title}
                        >

                            <div
                                className={`financial-kpi-icon ${card.className}`}
                            >
                                <Icon size={18} />
                            </div>

                            <div>

                                <div className="financial-kpi-value">
                                    {card.value}
                                </div>

                                <div className="financial-kpi-title">
                                    {card.title}
                                </div>

                                <div className="financial-kpi-subtitle">
                                    {card.subtitle}
                                </div>

                            </div>

                        </div>
                    );
                })}

            </div>


            {/* Revenue charts */}

            <div className="financial-chart-grid">

                {/* Insurance */}

                <div className="financial-card">

                    <div className="financial-card-header">

                        <div>

                            <div className="financial-card-title">
                                Revenue by Insurance
                            </div>

                            <div className="financial-card-subtitle">
                                Revenue distribution across insurance types
                            </div>

                        </div>

                        <div className="financial-card-icon blue">
                            <ShieldCheck size={16} />
                        </div>

                    </div>

                    <div className="financial-chart">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >

                            <BarChart
                                data={insuranceChart}
                                margin={{
                                    top: 10,
                                    right: 20,
                                    left: 5,
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
                                        fontSize: 8,
                                        fill: "#69758a",
                                    }}
                                />

                                <YAxis
                                    tickFormatter={(value) =>
                                        `₹${(
                                            value / 1000000
                                        ).toFixed(0)}M`
                                    }
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{
                                        fontSize: 8,
                                        fill: "#8994a7",
                                    }}
                                />

                                <Tooltip
                                    formatter={(value) =>
                                        money(value)
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
                                    dataKey="revenue"
                                    fill="#0ea5e9"
                                    radius={[
                                        5,
                                        5,
                                        0,
                                        0,
                                    ]}
                                    barSize={34}
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </div>

                </div>


                {/* Department */}

                <div className="financial-card">

                    <div className="financial-card-header">

                        <div>

                            <div className="financial-card-title">
                                Revenue by Department
                            </div>

                            <div className="financial-card-subtitle">
                                Highest revenue-generating departments
                            </div>

                        </div>

                        <div className="financial-card-icon purple">
                            <Building2 size={16} />
                        </div>

                    </div>

                    <div className="financial-chart">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >

                            <BarChart
                                data={revenueByDepartment}
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
                                    tickFormatter={(value) =>
                                        `₹${(
                                            value / 1000000
                                        ).toFixed(0)}M`
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
                                    formatter={(value) =>
                                        money(value)
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
                                    dataKey="total_revenue"
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


            {/* Payment status */}

            <div className="financial-bottom-grid">

                <div className="financial-card payment-card">

                    <div className="financial-card-header">

                        <div>

                            <div className="financial-card-title">
                                Payment Status
                            </div>

                            <div className="financial-card-subtitle">
                                Current billing payment distribution
                            </div>

                        </div>

                        <div className="financial-card-icon green">
                            <WalletCards size={16} />
                        </div>

                    </div>

                    <div className="payment-content">

                        <ResponsiveContainer
                            width="50%"
                            height={210}
                        >

                            <PieChart>

                                <Pie
                                    data={paymentChart}
                                    dataKey="value"
                                    nameKey="name"
                                    innerRadius={52}
                                    outerRadius={75}
                                    paddingAngle={3}
                                    stroke="none"
                                >

                                    {paymentChart.map(
                                        (_, index) => (
                                            <Cell
                                                key={index}
                                                fill={
                                                    paymentColors[
                                                        index %
                                                            paymentColors.length
                                                    ]
                                                }
                                            />
                                        )
                                    )}

                                </Pie>

                                <Tooltip />

                            </PieChart>

                        </ResponsiveContainer>


                        <div className="payment-list">

                            {paymentChart.map(
                                (item, index) => (
                                    <div
                                        className="payment-row"
                                        key={item.name}
                                    >

                                        <div>

                                            <span
                                                className="payment-dot"
                                                style={{
                                                    background:
                                                        paymentColors[
                                                            index %
                                                                paymentColors.length
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


                {/* Financial breakdown */}

                <div className="financial-card breakdown-card">

                    <div className="financial-card-header">

                        <div>

                            <div className="financial-card-title">
                                Financial Breakdown
                            </div>

                            <div className="financial-card-subtitle">
                                Revenue contribution
                            </div>

                        </div>

                        <div className="financial-card-icon orange">
                            <Receipt size={16} />
                        </div>

                    </div>


                    <div className="breakdown-list">

                        <div className="breakdown-item">

                            <div className="breakdown-label">
                                Insurance contribution
                            </div>

                            <div className="breakdown-value">
                                {summary
                                    ? (
                                          (Number(
                                              summary.insurance_covered
                                          ) /
                                              Number(
                                                  summary.total_revenue
                                              )) *
                                          100
                                      ).toFixed(1)
                                    : 0}
                                %
                            </div>

                            <div className="breakdown-bar">
                                <div
                                    style={{
                                        width: `${
                                            summary
                                                ? (
                                                      (Number(
                                                          summary.insurance_covered
                                                      ) /
                                                          Number(
                                                              summary.total_revenue
                                                          )) *
                                                      100
                                                  ).toFixed(1)
                                                : 0
                                        }%`,
                                    }}
                                />
                            </div>

                        </div>


                        <div className="breakdown-item">

                            <div className="breakdown-label">
                                Patient contribution
                            </div>

                            <div className="breakdown-value">
                                {summary
                                    ? (
                                          (Number(
                                              summary.patient_paid
                                          ) /
                                              Number(
                                                  summary.total_revenue
                                              )) *
                                          100
                                      ).toFixed(1)
                                    : 0}
                                %
                            </div>

                            <div className="breakdown-bar patient">
                                <div
                                    style={{
                                        width: `${
                                            summary
                                                ? (
                                                      (Number(
                                                          summary.patient_paid
                                                      ) /
                                                          Number(
                                                              summary.total_revenue
                                                          )) *
                                                      100
                                                  ).toFixed(1)
                                                : 0
                                        }%`,
                                    }}
                                />
                            </div>

                        </div>


                        <div className="financial-total">

                            <span>
                                Total Revenue
                            </span>

                            <strong>
                                {loading
                                    ? "..."
                                    : money(
                                          summary?.total_revenue
                                      )}
                            </strong>

                        </div>

                    </div>

                </div>

            </div>


            <div className="demo-note">
                <strong>Analytics note:</strong>{" "}
                Financial figures are based on the project's
                healthcare dataset and are intended for analytical
                demonstration.
            </div>

        </div>
    );
}

export default Financial;