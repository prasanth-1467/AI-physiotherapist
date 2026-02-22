'use client';

import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area
} from 'recharts';

const data = [
    { day: 'Mon', rom: 105, target: 145 },
    { day: 'Tue', rom: 108, target: 145 },
    { day: 'Wed', rom: 110, target: 145 },
    { day: 'Thu', rom: 112, target: 145 },
    { day: 'Fri', rom: 115, target: 145 },
    { day: 'Sat', rom: 118, target: 145 },
    { day: 'Sun', rom: 122, target: 145 },
];

export const RecoveryChart: React.FC = () => {
    return (
        <div className="w-full h-80">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                    <defs>
                        <linearGradient id="colorRom" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#2BBFBF" stopOpacity={0.1} />
                            <stop offset="95%" stopColor="#2BBFBF" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1A2B4A" strokeOpacity={0.05} />
                    <XAxis
                        dataKey="day"
                        axisLine={false}
                        tickLine={false}
                        tick={{ fill: '#1A2B4A', opacity: 0.4, fontSize: 12 }}
                        dy={10}
                    />
                    <YAxis
                        axisLine={false}
                        tickLine={false}
                        tick={{ fill: '#1A2B4A', opacity: 0.4, fontSize: 12 }}
                    />
                    <Tooltip
                        contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}
                    />
                    <Area
                        type="monotone"
                        dataKey="rom"
                        stroke="#2BBFBF"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorRom)"
                    />
                    <Line
                        type="monotone"
                        dataKey="target"
                        stroke="#1A2B4A"
                        strokeDasharray="5 5"
                        strokeOpacity={0.2}
                        dot={false}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};
