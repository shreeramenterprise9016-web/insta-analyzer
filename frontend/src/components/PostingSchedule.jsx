import React from 'react';

const PostingSchedule = ({ schedule }) => {
    if (!schedule || schedule.length === 0) return null;

    // Find max value for scaling
    const maxCount = Math.max(...schedule.map(d => d.count));

    // Format hour (e.g. 0 -> 12am, 13 -> 1pm)
    const formatHour = (h) => {
        if (h === 0) return '12am';
        if (h === 12) return '12pm';
        return h > 12 ? `${h - 12}pm` : `${h}am`;
    };

    return (
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h3 className="font-bold text-slate-800 mb-6 text-lg">Posting Schedule (UTC)</h3>

            <div className="flex justify-between gap-1 h-32 w-full">
                {schedule.map((slot) => {
                    // Calculate height percentage, min 4px for visibility
                    const heightPercent = maxCount > 0 ? (slot.count / maxCount) * 100 : 0;
                    const isActive = slot.count > 0;

                    return (
                        <div key={slot.hour} className="flex flex-col items-center justify-end flex-1 h-full group relative cursor-pointer">
                            {/* Tooltip */}
                            <div className="absolute bottom-full mb-2 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0 bg-gray-900 text-white text-[10px] font-medium rounded-md px-2 py-1 shadow-lg whitespace-nowrap z-10 pointer-events-none">
                                {formatHour(slot.hour)} • <span className="text-pink-300">{slot.count} posts</span>
                            </div>

                            {/* Bar Container */}
                            <div className="w-full px-[1px] h-full flex items-end">
                                <div
                                    className={`w-full rounded-t-md transition-all duration-500 ease-out group-hover:brightness-110 ${isActive ? 'bg-gradient-to-t from-pink-500 via-purple-500 to-indigo-500 shadow-md' : 'bg-gray-50'}`}
                                    style={{
                                        height: isActive ? `${Math.max(heightPercent, 10)}%` : '4px',
                                        minHeight: isActive ? '8px' : '4px'
                                    }}
                                ></div>
                            </div>

                            {/* Label */}
                            <span className={`text-[10px] mt-2 font-medium transition-colors ${slot.hour % 6 === 0 ? 'text-gray-400' : 'text-transparent group-hover:text-gray-300'}`}>
                                {slot.hour % 6 === 0 ? slot.hour : ''}
                            </span>
                        </div>
                    )
                })}
            </div>
            <div className="mt-4 text-center text-xs text-slate-500">
                Time of day (0-23h)
            </div>
        </div>
    );
};

export default PostingSchedule;
