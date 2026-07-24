import i18n from 'i18next';import {initReactI18next} from 'react-i18next';import en from './locales/en.json';import si from './locales/si.json';import ta from './locales/ta.json';
const saved=localStorage.getItem('platebridge-language')||'en';
i18n.use(initReactI18next).init({resources:{en:{translation:en},si:{translation:si},ta:{translation:ta}},lng:saved,fallbackLng:'en',interpolation:{escapeValue:false}});
i18n.on('languageChanged',lng=>{localStorage.setItem('platebridge-language',lng);document.documentElement.lang=lng});document.documentElement.lang=saved;
export default i18n;
