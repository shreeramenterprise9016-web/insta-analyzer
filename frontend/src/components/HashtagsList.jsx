import React from 'react';

function HashtagsList({ hashtags }) {
    if (!hashtags || hashtags.length === 0) return null;

    return (
        <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-100">
            <h3 className="text-lg font-bold text-dark mb-4">Top Hashtags</h3>
            <div className="flex flex-wrap gap-2">
                {hashtags.map((item, idx) => (
                    <span
                        key={idx}
                        className="px-3 py-1 bg-slate-100 text-slate-600 rounded-full text-sm font-medium"
                    >
                        #{item.tag} <span className="opacity-60 ml-1 text-xs">({item.count})</span>
                    </span>
                ))}
            </div>
        </div>
    );
}

export default HashtagsList;
