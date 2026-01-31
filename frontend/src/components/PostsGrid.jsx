import React from 'react';

function PostsGrid({ posts }) {
    return (
        <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-100">
            <h3 className="text-lg font-bold text-dark mb-4">Recent Uploads</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {posts.map((post, idx) => (
                    <div key={idx} className="group relative aspect-square bg-slate-100 rounded-lg overflow-hidden">
                        {/* Note: Actual post images might expire or be blocked. Using placeholder or if available */}
                        {/* If we had the image URL we would use it here. Instaloader gives URL but it expires... */}
                        {/* For Mock data we used placeholders. */}
                        <img
                            src={post.url.startsWith('http') ? post.url : 'https://via.placeholder.com/300'}
                            alt="Post"
                            className="w-full h-full object-cover transition-transform group-hover:scale-105"
                            onError={(e) => { e.target.src = 'https://via.placeholder.com/300?text=Image+Expired' }}
                        />

                        <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white gap-4 text-sm font-bold">
                            <div className="flex items-center gap-1">
                                <span>♥</span> {post.likes}
                            </div>
                            <div className="flex items-center gap-1">
                                <span>💬</span> {post.comments}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default PostsGrid;
