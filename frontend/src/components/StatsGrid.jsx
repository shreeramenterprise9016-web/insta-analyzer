import React from 'react';

function StatCard({ label, value, subtext, color = "blue" }) {
    const colorClasses = {
        blue: "bg-blue-50 text-blue-600",
        green: "bg-green-50 text-green-600",
        purple: "bg-purple-50 text-purple-600",
        orange: "bg-orange-50 text-orange-600",
    };

    return (
        <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100 flex flex-col items-center justify-center">
            <div className={`p-3 rounded-full mb-3 ${colorClasses[color]}`}>
                {/* Icon placeholder */}
                <div className="w-6 h-6 font-bold flex items-center justify-center">
                    {label[0]}
                </div>
            </div>
            <span className="text-2xl font-bold text-dark mb-1">{value}</span>
            <span className="text-sm text-slate-500 font-medium">{label}</span>
            {subtext && <span className="text-xs text-slate-400 mt-1">{subtext}</span>}
        </div>
    );
}

function StatsGrid({ stats }) {
    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
                label="Engagement Rate"
                value={`${stats.engagement_rate}%`}
                color="blue"
                subtext="High"
            />
            <StatCard
                label="Avg Likes"
                value={stats.avg_likes.toLocaleString()}
                color="green"
                subtext="Per Post"
            />
            <StatCard
                label="Avg Comments"
                value={stats.avg_comments.toLocaleString()}
                color="purple"
                subtext="Per Post"
            />
            <StatCard
                label="Uploads/Week"
                value={stats.uploads_per_week}
                color="orange"
                subtext="Estimated"
            />
        </div>
    );
}

export default StatsGrid;
