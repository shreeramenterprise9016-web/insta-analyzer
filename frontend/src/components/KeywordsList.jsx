const KeywordsList = ({ keywords }) => {
    if (!keywords || keywords.length === 0) return null;

    return (
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h3 className="font-bold text-slate-800 mb-4 text-lg">Top Keywords</h3>
            <div className="flex flex-wrap gap-2">
                {keywords.map((kw, index) => (
                    <div
                        key={index}
                        className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium border border-blue-100 flex items-center gap-2"
                    >
                        <span>{kw.word}</span>
                        <span className="bg-blue-200 text-blue-800 text-xs px-1.5 py-0.5 rounded-full">{kw.count}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default KeywordsList;
