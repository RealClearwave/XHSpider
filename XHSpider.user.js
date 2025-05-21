// ==UserScript==
// @name         XHSpider
// @namespace    https://github.com/JoeanAmier/XHS-Downloader
// @version      2.0.2
// @description  爬取小红书数据（增加“等待评论加载”）
// @author       Clearwave
// @match        http*://xhslink.com/*
// @match        http*://www.xiaohongshu.com/explore*
// @match        http*://www.xiaohongshu.com/user/profile/*
// @match        http*://www.xiaohongshu.com/search_result*
// @match        http*://www.xiaohongshu.com/board/*
// @icon         data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAEIUExURUdwTPNIRO5CPug8OO5CPfhLRPxGROk8OP9XU/NHQ/FEQOg8OO9DP+c6Nug7N+5BPe1APPFFQO9DPvVIROc7NuU5Nek8OPNGQu9CPvJFQek8OO9CPuk8OO9CPuU4NO5CPuU4NO9CPv///uU5Nf///9YqJtQoJOQ4NPizsf/599UvK++Rj+BXVP/r6uh3dOM2Mt4yLuk9OdwvK9crJ+2LieNkYdcsKOE0MPasqtpEQPOgnuNrZ9czL+uBftotKfSlo+FeW+yHhOdzcPGdmvCUkfq6uOl9et1LR+ZwbfGYlv/n5vzBv/7Rz+t5dtk7N9EkIP3Hxf/i4N5STv/08v/b2cwfG//v7v/8+vNjnHUAAAAidFJOUwAVnPOIDgf7Ai9S1Ui+5GpyX6gizKvrPbR7k8Dez9zd9+hDReWtAAAHR0lEQVR42sWbCVuiXBiGj/ta5m5m00wH0NQUFBAX3Nc0y7b5///kO/g1nSRZRIT76rpy4g1uznmfIyMEjOENhCPubDJ5hkgms+5IMOABFuEIX8ZufDCPgBB9IbavmT8Zd9ABTos37L72QRWYG2fQc7KjB2MuqANfJnoKh7TTBXXji4X95p589JqBh5G7MG8YPBfn0AAut8Ocs79IQYQxheNHwR/NwSNIRY7shcAZPJJQ+pjRd/vg0TBOj+HTD0FTOA8bm/0LHzQJxu01kL0MNJFE/ODhz0FTSR3Yi2EXNBkmCg4g4oOmw7j1LwmXDDwFTp0GfjcDT0NSXxjc8GQk/QbG3+pZiDDwhOTdQIOgD54UJqKx/rjgiWHCQAVHDp4cV1wlgGfQAkIe5QBAS3ACBdI+aAlMEOzFk4MWkXJYvQLKyexNIJ4AWybBn4AWcv4zCRFoKe4fHZiCluKL29OBmJhsDXZBi/EF5ANg6xB48ADY0wUXUJNqg6ZrW2i6UYV7yFdlFRpkwRf+nMbB6Vq9+DJkW0KhILTY+Qtfr9HVXb0aT87mg5FU0StVyh1coYQLrwVhqArdmQsPxA4bYd7p0tV/fl2ea73tVtwXHtd0HqqBL44y6udfJiRuv0FIPA/5WlU6PMlN9lcMG1CN668M+qAajTLe9+4h/i7WjUaH/SAUCh5pqAYTwKuwhsAtRubAd6XJUdhcofWtx1fKoy+hLIAMKPIebVUUqEpAJXJ+jRlozJrNWZM2LlBbS3tQ7oQAkIhCJboEYsJ/ChDfkAns3Y4E+AWB6EAlLoFEDCpB3qFfL5D/CxAfC3HO9bnhoLeSDrYrQCBWAjtEBe3peEP8L0CWCERRMY1XAOFPqQncYoH2E/kPasaiTVgAvViUqa/NTzMsgL4pC/iktSgOdQqs2mihE3oLsd+hyKfSrkDhnaSK5cdxSxBGbHuiUwCGcQuoCsjn+KFXud8VuJuONgRGWwAH0alLQJ7/fT0gL8MCqpfH15oChmOoLfAH9aBLU8BwDLUFGAfuQc0mfO2xlXl7Ph0X3vZPwWayEIftdmXQetDbAzCM34r1xxBRXtzKYtjjitRXDJt6BfIRENEtsOxPS6PWgh2+8CT5PtoVmLxLq8N8sGiNxiInaArgGLh1C3zjbdGWx3BeWhmIYT6JUmhnDOEZSEI7Y5gPgTNoZwzhOUjoj6GwECvDKdtaPuyfgvvnHjsdVsSScK+7B1zgl24B7iuGVKfdI2QxLMw7BmIIfx8gUHiZD8ZjVuSaFIphb1fgWYrhmpuy4/GgUh7pFoAHCHxjxfYfZDFsi893uOAUAhhCKYbE4THMg5A9McQ9kLA1hvmU/nWAuJu0SqI4WAir1/1TcLcqLFhRZEeFD9098AskdQv0cQzXlYI8hstp08i7YQJkdQsITW46GIjDcoeqk+/CrsDqnaxTnfJcHAym7RmrewSS4MJADF+X07I8hv3K5MNADLMgaG8ML0DA3nfDIPD67BSAAQBu7BTweQGI2Slwje/TqAqgbzJ+CPysIHQIOJFAWocA4mHZGgzbHIcu+6UrEgksQPy7HqmgCm4ojiYbAvGoKRAFAHWhhkC9v1n0ixRZr9fJLXWSKvYXbwRiK4DYtDipgpTYFlJkmX175DUEmDhAXGkIdOmutMcmJ/23oDcqTftNyYZaD5ADWf8g7ktNSqpY9x/ZUa/XGovctqJL1zQEboDEpYbAE8/3Rytih9WoT9V56mVZqxX6FF+nXsbPf3cq3nrtIk9pCDiBREBd4JYtEFvkS2GBo/hatUp3qRfhDld8K1myr+oCQfxJsaLALd7zj9cfbLHbJR83+Mf7qpGAxqfFbmUBvF85n5+VCr3Xr3/sS6qqQAxs8QcYdYFtxiYDrlmkEJ0Zx04+sMM2joi7Zak961CIYrMvFrZJ1RAIgk+u1XoAsRo0yS7dqFa3dwWqDTTtTRZFAC9BD+MZ1aVRSV4qQRU1cj193joQigIpr9b9irrU2M/imqersn3kG3S92SM+KbyQtYa8AnVnZ7gkEB0FgSzQ+ricFp4r+LYAlDvUOuMNOvnWuis/OsQ3EtqTZU3jw3KEU/FOCT763u08haLYgJgDdnEFMKgNrScIvpGBlhPyA3uHIAh2yNg5APjpATufIHBCS7kCchwuu25d4+XQQrLA3mc4zj32PsXChG15kArjVHmUzN6HyeIpexKACSu0gXUPGF9a3gCWL4hnXqCK98yeBsR4Troe5eJAE0fohCsgOr6dBucBoAtHwp7xx3hO0omhONCNN3aC/DnAIZj9iD/j9ILDCLpMXf8j4GDiCRPbL23D31lhmJgHGMKfzkETSAVt/WMzxukAxxC4Oi4OiTQ4lnDoiOaL+sHx+KMGFc4jXmAO/qCBiQhFvcBEAk7XQQtPLO0HJuOJZnw6j34VwZ1vskMsBTVwZdDRT4g/cBG7YRQi/ydzmfYCC3CkI9lk4tdv+Mnv80QyGwkbOvP/AM/hIrquHOjjAAAAAElFTkSuQmCC
// @license      GNU General Public License v3.0
// @run-at       document-end
// ==/UserScript==

(function () {
    'use strict';

    // 等待 parent-comment 节点出现再执行
    function waitForComments(timeout = 10000, interval = 200) {
        return new Promise((resolve, reject) => {
            const start = Date.now();
            const timer = setInterval(() => {
                if (document.getElementsByClassName("parent-comment").length > 0) {
                    clearInterval(timer);
                    resolve();
                } else if (Date.now() - start > timeout) {
                    clearInterval(timer);
                    reject(new Error("等待 parent-comment 超时"));
                }
            }, interval);
        });
    }

    // 用户主页逻辑（不变）
    if (window.location.href.includes("https://www.xiaohongshu.com/user/profile/")) {
        // 输出用户简介
        if (document.getElementsByClassName('user-desc').length > 0) {
            console.warn("GerenJianjie " + document.getElementsByClassName('user-desc')[0].innerText);
        } else {
            console.warn("GerenJianjie无");
        }
        // 获取点赞数最高的笔记
        const notes = document.getElementsByClassName("note-item");
        if (notes.length === 0) {
            console.warn("无有效链接");
            return;
        }
        let parent_id = 0, max_cnt = -1;
        for (let i = 0; i < notes.length; i++) {
            let cur_cnt = notes[i].getElementsByClassName("count")[0].innerText;
            if (cur_cnt.endsWith("万")) {
                cur_cnt = parseFloat(cur_cnt) * 10000;
            } else {
                cur_cnt = parseInt(cur_cnt, 10);
            }
            if (cur_cnt > max_cnt) {
                max_cnt = cur_cnt;
                parent_id = i;
            }
        }
        const note_link = "https://www.xiaohongshu.com/explore/" +
            notes[parent_id].getElementsByClassName("cover mask ld")[0].href.split("/")[6];
        console.warn(note_link);
    }

    // 笔记详情页：先等待评论加载，再执行
    if (window.location.href.includes("https://www.xiaohongshu.com/explore/")) {
        waitForComments().then(() => {
            const comments = document.getElementsByClassName("parent-comment");
            let parent_id = 0, max_cnt = 0;

            for (let i = 0; i < comments.length; i++) {
                const blk = comments[i];
                const itxt = blk.getElementsByClassName("note-text")[0]?.innerText;
                if (!itxt) continue;
                if (!blk.getElementsByClassName("reply-container").length) continue;
                const picCnt = blk.getElementsByClassName("comment-picture").length;
                if (picCnt > max_cnt) {
                    max_cnt = picCnt;
                    parent_id = i;
                }
            }

            const w_msg = {};
            const chosen = comments[parent_id];

            // 评论内容 & 用户主页
            w_msg.comment_content = chosen.getElementsByClassName("note-text")[0]?.innerText || "无";
            w_msg.comment_user_homepage = chosen.getElementsByClassName("avatar")[0]?.children[0]?.href || "无";

            // 是否有回复
            const replyContainer = chosen.getElementsByClassName("reply-container")[0];
            const have_reply = !!replyContainer;

            // 评论多模态
            const cPics = chosen.getElementsByClassName("comment-picture");
            if (cPics.length > 0) {
                w_msg.is_comment_multimodal = true;
                w_msg.comment_multimodal_url = cPics[0].querySelector(".inner")?.src || "无";
            } else {
                w_msg.is_comment_multimodal = false;
                w_msg.comment_multimodal_url = "无";
            }

            // 回复内容 & 多模态
            if (have_reply) {
                w_msg.have_reply = true;
                w_msg.reply_content = replyContainer.getElementsByClassName("note-text")[0]?.innerText || "无";
                const rPics = replyContainer.getElementsByClassName("comment-picture");
                if (rPics.length > 0) {
                    w_msg.is_reply_multimodal = true;
                    w_msg.reply_multimodal_url = rPics[0].querySelector(".inner")?.src || "无";
                } else {
                    w_msg.is_reply_multimodal = false;
                    w_msg.reply_multimodal_url = "无";
                }
            } else {
                w_msg.have_reply = false;
                w_msg.reply_content = "无";
                w_msg.is_reply_multimodal = false;
                w_msg.reply_multimodal_url = "无";
            }

            console.warn(JSON.stringify(w_msg));
        }).catch(err => {
            console.error("评论等待失败：", err);
        });
    }
})();
