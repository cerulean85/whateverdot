
export const STATE_WAITING         = 'waiting';
export const STATE_PROBING         = 'probing';
// export const STATE_PROBE_STOPPED   = 'probe_stopped';
export const STATE_COLLECTING      = 'collecting';
// export const STATE_COLLECT_STOPPED = 'collect_stopped';
export const STATE_PROCESSING      = 'processing';
export const STATE_PAUSED          = 'paused';
export const STATE_STOPPED         = 'stopped';
export const STATE_FINISHED        = 'finished';
export const STATE_TERMINATED      = 'terminated';
export const STATE_ERROR           = 'error';

export const StateExpression = {
    'waiting': { state:'waiting', label: '대기', backgroundColor: '#00b050', width: 100 },
    'collect_url': { state:'collect_url', label: '링크 수집중', backgroundColor: '#00b050', width: 100 },
    'collect_doc': { state:'collect_doc', label: '웹 페이지 수집중', backgroundColor: '#FF4E00', width: 100 },
    'extract_text': { state:'extract_text', label: '텍스트 수집중', backgroundColor: '#0070c0', width: 100 },
    'extract_content': { state:'extract_content', label: '본문 수집중', backgroundColor: '#ff9e01', width: 100 },
    'stopped': { state:'stop', label: '정지', backgroundColor: '#FF4E00', width: 100 },
    'finished': { state:'finished', label: '완료', backgroundColor: '#0046C0', width: 100 },
    'error': { state:'error', label: '오류', backgroundColor: '#ff9e01',width: 100 }
};

export const Images = {
    'processing': process.env.PUBLIC_URL + '/button_process',
    'paused': process.env.PUBLIC_URL + '/button_pause',
    'stopped': process.env.PUBLIC_URL + '/button_stop',
    'terminated': process.env.PUBLIC_URL + '/button_terminate',
    'addWork': process.env.PUBLIC_URL + '/button_add_work.svg',
    'close': process.env.PUBLIC_URL + '/button_close.svg',
};

export const CollectTargetName = {
    'naver': '네이버',
    'daum': '다음',
    'chosun': '조선일보',
    'joongang': '중앙일보',
    'donga': '동아일보',
    'tweeter': '트위터',
    'facebook': '페이스북',
    'naver_blog': '네이버 블로그'
}
// export const ButtonControl = process.env.PUBLIC_URL + '/button_process.svg';