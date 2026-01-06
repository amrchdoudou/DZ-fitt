import { reactive } from 'vue';

const translations = {
    en: {
        navbar: {
            home: 'Home',
            search: 'Search',
            how_it_works: 'How it works',
            about_us: 'About us',
            login: 'Log in',
            signup: 'Sign Up',
            logout: 'Log out'
        },
        hero: {
            title: 'Make the perfect\ngym for you',
            subtitle: 'DZ-Fit helps you discover, compare, and choose the gym that fits your goals.',
            placeholder: 'Enter an address or area',
            search_btn: 'Search',
            location_btn: 'Enable location'
        },
        how_it_works: {
            title: 'How It Works ?',
            subtitle: 'A simple flow to help you discover and manage gyms in Algeria.',
            steps: [
                { title: 'Search nearby gyms', desc: 'Use your location or type an address to see gyms and fitness spaces around you.' },
                { title: 'Filter & explore', desc: 'Refine results by services, equipment, classes, and opening hours to find a fit.' },
                { title: 'View gym details', desc: 'Check photos, descriptions, equipment lists, and contact info in one place.' },
                { title: 'Create your gym', desc: 'Gym owners can set up a profile with photos, services, and location in minutes.' },
                { title: 'Add courses', desc: 'Highlight classes and programs with schedules so members know what to join.' },
                { title: 'Keep everything updated', desc: 'Edit your info anytime so users always see current details and offerings.' }
            ]
        },
        about: {
            title: 'About Us',
            p1: 'DZ-Fit is the first intelligent gym directory in Algeria, designed to help users find the perfect fitness space based on their location, needs, and training style.',
            p2: 'We make it easy for people to search, compare, and explore gyms across the country with clear, reliable, and structured information.',
            mission: 'Our mission is simple: connect Algerians with the right gym, instantly.'
        },
        search_result: {
            title: 'Search Results',
            no_results: 'No gyms found in this area.',
            loading: 'Searching for gyms...',
            filters: 'Filters',
            apply: 'Apply Filters'
        },
        management: {
            dashboard: 'Dashboard',
            my_gym: 'My gym',
            reviews: 'Reviews',
            courses: 'Courses',
            settings: 'Settings',
            add_gym: 'Add Gym',
            gym_label: 'Gym',
            improve_profile: 'Improve Your Gym Profile',
            improve_desc: 'Fill missing details like amenities to improve visibility.',
            create_class: 'Create Your First Class',
            create_desc: 'Help users discover what you offer.'
        }
    },
    fr: {
        navbar: {
            home: 'Accueil',
            search: 'Recherche',
            how_it_works: 'Comment ça marche',
            about_us: 'À propos',
            login: 'Connexion',
            signup: 'S\'inscrire',
            logout: 'Déconnexion'
        },
        hero: {
            title: 'Créez la salle de\nsport parfaite pour vous',
            subtitle: 'DZ-Fit vous aide à découvrir, comparer et choisir la salle de sport qui correspond à vos objectifs.',
            placeholder: 'Entrez une adresse ou une ville',
            search_btn: 'Rechercher',
            location_btn: 'Ma position'
        },
        how_it_works: {
            title: 'Comment ça marche ?',
            subtitle: 'Un flux simple pour vous aider à découvrir et gérer les salles de sport en Algérie.',
            steps: [
                { title: 'Recherchez des salles', desc: 'Utilisez votre position ou tapez une adresse pour voir les salles autour de vous.' },
                { title: 'Filtrez et explorez', desc: 'Affinez les résultats par services, équipements et horaires pour trouver l\'idéal.' },
                { title: 'Voir les détails', desc: 'Consultez les photos, descriptions, listes d\'équipements et infos de contact.' },
                { title: 'Créez votre salle', desc: 'Les propriétaires peuvent configurer un profil avec photos et services en quelques minutes.' },
                { title: 'Ajoutez des cours', desc: 'Mettez en avant vos classes et programmes avec des horaires précis.' },
                { title: 'Gardez tout à jour', desc: 'Modifiez vos infos à tout moment pour que les utilisateurs voient les détails personnels.' }
            ]
        },
        about: {
            title: 'À propos de nous',
            p1: 'DZ-Fit est le premier annuaire intelligent de salles de sport en Algérie, conçu pour aider les utilisateurs à trouver l\'espace de fitness parfait.',
            p2: 'Nous facilitons la recherche, la comparaison et l\'exploration des salles à travers le pays avec des informations fiables.',
            mission: 'Notre mission est simple : connecter les Algériens à la bonne salle de sport, instantanément.'
        },
        search_result: {
            title: 'Résultats de recherche',
            no_results: 'Aucune salle trouvée dans cette zone.',
            loading: 'Recherche de salles...',
            filters: 'Filtres',
            apply: 'Appliquer'
        },
        management: {
            dashboard: 'Tableau de bord',
            my_gym: 'Ma salle',
            reviews: 'Avis',
            courses: 'Cours',
            settings: 'Paramètres',
            add_gym: 'Ajouter une salle',
            gym_label: 'Salle',
            improve_profile: 'Améliorez le profil de votre salle',
            improve_desc: 'Complétez les détails comme les équipements pour améliorer la visibilité.',
            create_class: 'Créez votre premier cours',
            create_desc: 'Aidez les utilisateurs à découvrir vos offres.'
        }
    },
    ar: {
        navbar: {
            home: 'الرئيسية',
            search: 'بحث',
            how_it_works: 'كيف يعمل',
            about_us: 'من نحن',
            login: 'تسجيل الدخول',
            signup: 'إنشاء حساب',
            logout: 'تسجيل الخروج'
        },
        hero: {
            title: 'ابحث عن قاعة\nالرياضة المثالية بالقرب منك',
            subtitle: 'DZ-Fit يساعدك على اكتشاف ومقارنة واختيار قاعة الرياضة التي تناسب أهدافك.',
            placeholder: 'أدخل العنوان أو المنطقة',
            search_btn: 'بحث',
            location_btn: 'تفعيل الموقع'
        },
        how_it_works: {
            title: 'كيف يعمل ؟',
            subtitle: 'مسار بسيط لمساعدتك في اكتشاف وإدارة قاعات الرياضة في الجزائر.',
            steps: [
                { title: 'بحث عن القاعات', desc: 'استخدم موقعك أو اكتب عنواناً لرؤية قاعات الرياضة من حولك.' },
                { title: 'تصفية واستكشاف', desc: 'صَفِّ النتائج حسب الخدمات والمعدات والحصص والحلول للعثور على الأنسب.' },
                { title: 'عرض التفاصيل', desc: 'تحقق من الصور والأوصاف وقوائم المعدات ومعلومات الاتصال في مكان واحد.' },
                { title: 'أنشئ قاعتك', desc: 'يمكن لأصحاب القاعات إعداد ملف شخصي مع الصور والخدمات والموقع في دقائق.' },
                { title: 'أضف حصصاً', desc: 'أبرز الحصص والبرامج مع الجداول حتى يعرف الأعضاء ما يمكنهم الانضمام إليه.' },
                { title: 'حافظ على التحديث', desc: 'قم بتعديل معلوماتك في أي وقت حتى يرى المستخدمون دائماً أحدث التفاصيل.' }
            ]
        },
        about: {
            title: 'من نحن',
            p1: 'DZ-Fit هو أول دليل ذكي لقاعات الرياضة في الجزائر، مصمم لمساعدة المستخدمين في العثور على المساحة المثالية.',
            p2: 'نجعل من السهل على الأشخاص البحث والمقارنة واستكشاف القاعات في جميع أنحاء البلاد بمعلومات موثوقة.',
            mission: 'مهمتنا بسيطة: ربط الجزائريين بالقاعة الرياضية المناسبة فوراً.'
        },
        search_result: {
            title: 'نتائج البحث',
            no_results: 'لم يتم العثور على قاعات في هذه المنطقة.',
            loading: 'جاري البحث عن قاعات...',
            filters: 'الفلاتر',
            apply: 'تطبيق'
        },
        management: {
            dashboard: 'لوحة التحكم',
            my_gym: 'قاعتي',
            reviews: 'المراجعات',
            courses: 'الدروس',
            settings: 'الإعدادات',
            add_gym: 'إضافة قاعة',
            gym_label: 'قاعة',
            improve_profile: 'حسن ملف قاعتك الرياضية',
            improve_desc: 'أكمل التفاصيل المفقودة مثل المرافق لتحسين الظهور.',
            create_class: 'أنشئ أول حصة لك',
            create_desc: 'ساعد المستخدمين على اكتشاف ما تقدمه.'
        }
    }
};

export const i18n = reactive({
    locale: localStorage.getItem('siteLang') || 'fr',

    t(path) {
        const keys = path.split('.');
        let result = translations[this.locale];

        for (const key of keys) {
            if (result && result[key]) {
                result = result[key];
            } else {
                // Fallback to FR if key missing in current locale
                let fallback = translations['fr'];
                for (const fKey of keys) {
                    if (fallback && fallback[fKey]) fallback = fallback[fKey];
                    else return path;
                }
                return fallback;
            }
        }
        return result;
    },

    setLocale(lang) {
        this.locale = lang;
        localStorage.setItem('siteLang', lang);
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
        document.documentElement.lang = lang;
    }
});

// Sync initial state
document.documentElement.dir = i18n.locale === 'ar' ? 'rtl' : 'ltr';
document.documentElement.lang = i18n.locale;
