import React from 'react';

function ProfileHeader({ profile }) {
    return (
        <div className="bg-white rounded-xl shadow-sm p-6 flex flex-col md:flex-row items-center md:items-start gap-6 border border-slate-100">
            <div className="flex-shrink-0">
                <img
                    src={profile.profile_pic_url}
                    alt={profile.username}
                    className="w-24 h-24 rounded-full border-4 border-slate-50 object-cover shadow-sm"
                />
            </div>
            <div className="flex-1 text-center md:text-left">
                <div className="flex items-center justify-center md:justify-start gap-2 mb-2">
                    <h2 className="text-2xl font-bold text-dark">{profile.full_name}</h2>
                    {profile.is_verified && (
                        <span className="text-blue-500" title="Verified">
                            <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-1.9 14.7L6 12.6l1.5-1.5 2.6 2.6 6.4-6.4 1.5 1.5-7.9 7.9z"></path></svg>
                        </span>
                    )}
                    <span className={`px-2 py-0.5 text-xs font-bold rounded-full border ${profile.is_mock ? 'bg-yellow-50 text-yellow-700 border-yellow-200' : 'bg-green-50 text-green-700 border-green-200'}`}>
                        {profile.is_mock ? 'MOCK DATA' : 'REAL DATA'}
                    </span>
                </div>
                {profile.is_mock && profile.error_message && (
                    <div className="mb-4 p-2 bg-red-50 text-red-600 text-xs rounded border border-red-100">
                        <strong>Scraping Error:</strong> {profile.error_message}
                        {profile.error_message.includes("Invalid OAuth") && (
                            <div className="mt-1 font-bold text-red-700">
                                Action Required: Your API Token is invalid/expired. Please generate a new System User Access Token in Facebook Developer Portal.
                            </div>
                        )}
                    </div>
                )}
                <p className="text-slate-500 font-medium mb-4">@{profile.username}</p>
                <p className="text-slate-600 mb-6 text-sm max-w-lg mx-auto md:mx-0 whitespace-pre-wrap">
                    {profile.biography}
                </p>

                <div className="flex justify-center md:justify-start gap-8 border-t pt-4">
                    <div className="text-center">
                        <span className="block text-lg font-bold text-dark">{profile.followers.toLocaleString()}</span>
                        <span className="text-xs text-slate-400 uppercase tracking-wider">Followers</span>
                    </div>
                    <div className="text-center">
                        <span className="block text-lg font-bold text-dark">{profile.followees.toLocaleString()}</span>
                        <span className="text-xs text-slate-400 uppercase tracking-wider">Following</span>
                    </div>
                    <div className="text-center">
                        <span className="block text-lg font-bold text-dark">{profile.mediacount.toLocaleString()}</span>
                        <span className="text-xs text-slate-400 uppercase tracking-wider">Posts</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ProfileHeader;
