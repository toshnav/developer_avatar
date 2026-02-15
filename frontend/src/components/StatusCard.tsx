import React from 'react';

interface StatusCardProps {
    title: string;
    value: string | number;
    colorClass: string;
}

export const StatusCard: React.FC<StatusCardProps> = ({ title, value, colorClass }) => {
    return (
        <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-lg">
            <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-1">{title}</h3>
            <p className={`text-2xl font-bold ${colorClass}`}>
                {value}
            </p>
        </div>
    );
};
