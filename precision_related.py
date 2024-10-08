#-*- coding: UTF-8 -*-
from sklearn.preprocessing import normalize
from custom_setting import *
from name import *
from difflib import SequenceMatcher
import re
import fuzzy

normalized_feature_dict = {}
soundex = fuzzy.Soundex(4)


def is_substr(s1, s2):
    """return whether srtring s1 appear in string in s2"""
    return bool(re.search(".*".join(s1), s2)) or bool(re.search(".*".join(s2), s1))


def my_string_match_score(s1, s2, name_statistics, is_asian=False):
    """Give a score for similarity between s1 and s2"""
    elements_s1 = s1.split()
    elements_s2 = s2.split()
    if len(elements_s1) > len(elements_s2):
        elements_s1 = s2.split()
        elements_s2 = s1.split()
    count = 0
    rare_count = 0
    full_score = len(elements_s1)
    for element1 in elements_s1:
        flag = False
        candi = ""
        for element2 in elements_s2:
            if len(element1) != 1 and len(element2) != 1:
                if element2 != element1:
                    if element2 in element1:
                        idx = elements_s2.index(element2)
                        if len(elements_s2) > idx + 1:
                            if element2 + elements_s2[idx + 1] == element1 \
                                    or (SequenceMatcher(None, element1, element2 + elements_s2[idx + 1]).ratio() >= 0.9
                                        and len(element2) >= 3 and len(elements_s2[idx + 1]) >= 3) \
                                    or (element1, element2 + elements_s2[idx + 1]) in nickname_set:
                                count += 2
                                elements_s2.remove(elements_s2[idx + 1])
                                elements_s2.remove(element2)
                                # print 1
                                break
                        if idx >= 1:
                            if elements_s2[idx - 1] + element2 == element1 \
                                    or (SequenceMatcher(None, element1, elements_s2[idx - 1] + element2).ratio() >= 0.9
                                        and len(element2) >= 3 and len(elements_s2[idx - 1]) >= 3) \
                                    or (element1, elements_s2[idx - 1] + element2) in nickname_set:
                                count += 3
                                elements_s2.remove(elements_s2[idx - 1])
                                elements_s2.remove(element2)
                                # print 2
                                break
                    elif element1 in element2:
                        idx = elements_s1.index(element1)
                        if len(elements_s1) > idx + 1:
                            if element1 + elements_s1[idx + 1] == element2 \
                                    or (SequenceMatcher(None, element2, element1 + elements_s1[idx + 1]).ratio() >= 0.9
                                        and len(element1) >= 3 and len(elements_s1[idx + 1]) >= 3) \
                                    or (element2, element1 + elements_s1[idx + 1]) in nickname_set:
                                count += 3
                                elements_s2.remove(element2)
                                elements_s1.remove(elements_s1[idx + 1])
                                # print 3
                                break
                        if idx >= 1:
                            if elements_s1[idx - 1] + element1 == element2 \
                                    or (SequenceMatcher(None, element1, elements_s1[idx - 1] + element1).ratio() >= 0.9
                                        and len(element1) >= 3 and len(elements_s1[idx - 1]) >= 3) \
                                    or (element2, elements_s1[idx - 1] + element1) in nickname_set:
                                count += 3
                                elements_s2.remove(element2)
                                elements_s1.remove(elements_s1[idx - 1])
                                # print 4
                                break
                if is_asian:
                    if SequenceMatcher(None, element1, element2).ratio() > 0.90:
                        if element1 == element2 and element1 in name_statistics and (name_statistics[element1] <= 10 or name_statistics[element2] <= 10):
                            count += 1
                            rare_count += 1
                        else:
                            count += 1
                        if flag is True:
                            flag = False
                        elements_s2.remove(element2)
                        break
                else:
                    tmp1 = element1.lower()
                    tmp2 = element2.lower()
                    ldis = SequenceMatcher(None, tmp1, tmp2).ratio()
                    if ldis > 0.88 or \
                            (ldis > 0.80 and abs(int(soundex(tmp1)[1:]) - int(soundex(tmp2)[1:])) <= 2):
                        if tmp1 == tmp2 and tmp1 in name_statistics and (name_statistics[element1] <= 10 or name_statistics[element2] <= 10):
                            count += 1
                            rare_count += 1
                        else:
                            count += 1
                        if flag is True:
                            flag = False
                        elements_s2.remove(element2)
                        break
            # print  (element1, element2)
            if (element1, element2) in nickname_set:
                count += 1
                elements_s2.remove(element2)
                break
            if element1 == '' or element2 == '':
                continue
            if len(element1) == 1 and len(element2) == 1 and element1 == element2:
                count += 1
                elements_s2.remove(element2)
                break
            if (element1, element2) in nickname_initials_set:
                flag = True
                candi = element2
                continue
            if element1[0] != element2[0]:
                continue
            if len(element1) == 1 and len(element2) == 1:
                count += 1
                elements_s2.remove(element2)
                break
            if len(element1) == 1 and len(element2) != 1:
                if flag is True:
                    continue
                flag = True
                candi = element2
            if len(element1) != 1 and len(element2) == 1:
                if flag is True:
                    continue
                flag = True
                candi = element2
            # if element2.find(element1) >= 0 or element1.find(element2) >= 0:
            #     if flag is True:
            #         continue
            #     flag = True
            #     candi = element2
        else:
            if flag is True:
                count += 0.49
                elements_s2.remove(candi)
                continue
            count -= 0.26
        # print element1 + ' ' + element2 + ' ' + str(count)
    elements_s1 = s1.split(" ")
    elements_s2 = s2.split(" ")

    #Specific operations on noisy last names.
    if elements_s1[-1] != elements_s2[-1]:
        if is_asian:
            if SequenceMatcher(None, elements_s1[-1], elements_s2[-1]).ratio() <= 0.90:
                if elements_s1[-1][:-1] == elements_s2[-1][:-1] \
                        or elements_s1[-1][:-1] == elements_s2[-1] \
                        or elements_s1[-1] == elements_s2[-1][:-1]:
                    count += 1.5
        else:
            element1 = elements_s1[-1].lower()
            element2 = elements_s2[-1].lower()
            ldis = SequenceMatcher(None, element1, element2).ratio()
            if ldis <= 0.85 and \
                    (ldis <= 0.80 or abs(int(soundex(element1)[1:]) - int(soundex(element2)[1:])) > 2):
                if elements_s1[-1][:-1] == elements_s2[-1][:-1] \
                        or elements_s1[-1][:-1] == elements_s2[-1] \
                        or elements_s1[-1] == elements_s2[-1][:-1]:
                    count += 1.5

            # if element1.find(element2) == 0:
            #     if element1[len(element2):] not in 'andyzt':
            #         return 0
            # if element2.find(element1) == 0:
            #     if element2[len(element1):] not in 'andyzt':
            #         return 0
    # print full_score
    # print count
    if count == full_score or count >= 4 or rare_count >= 2:
        return 100
    return count


def single_name_comparable(name_instance_A, name_instance_B, name_statistics):
    """Decide whether two name instances are comparable"""
    name_A = name_instance_A.name
    name_B = name_instance_B.name

    if name_instance_A.is_asian and name_instance_B.is_asian:
        # Han Liu and Huan Liu
        if name_instance_A.middle_name == '' and name_instance_B.middle_name == '':
            if len(name_instance_A.first_name) > 1 and len(name_instance_B.first_name) > 1:
                if name_instance_A.first_name != name_instance_B.first_name:
                    return False
        # Han Liu  and H. L. Liu
        if len(name_instance_A.first_name) == 1 and len(name_instance_A.middle_name) == 1:
            if not is_substr(name_A.replace(' ', ''), name_B):
                return False
        if len(name_instance_B.first_name) == 1 and len(name_instance_B.middle_name) == 1:
            if not is_substr(name_A, name_B.replace(' ', '')):
                return False
        # Lin Yu, Lin Yi
        if name_instance_A.last_name != name_instance_B.last_name:
            return False

    if name_B.find(name_A.replace(' ', '')) >= 0 or name_A.find(name_B.replace(' ', '')) >= 0:
        return True

    index = max(name_B.find(name_A), name_A.find(name_B))
    if index >= 0:
        string1 = max(name_A, name_B, key=len)
        string2 = min(name_A, name_B, key=len)
        if index > 0:
            if string1[index - 1] == ' ':
                return True
        else:
            if (index + len(string2)) <= len(string1) - 1:
                if string1[index + len(string2)] == ' ' or string1[index + len(string2):] == 'and' \
                        or string1[index + len(string2):] == 'yz' or string1[index + len(string2):] == 't' \
                        or string1[index + len(string2):] == 'z':
                    return True

    if name_A.replace(' ', '') == name_B.replace(' ', ''):
        return True

    score = my_string_match_score(name_instance_A.name, name_instance_B.name, name_statistics, name_instance_A.is_asian or name_instance_B.is_asian)
    # print name_instance_A.name + '   ' + name_instance_B.name + str(score)
    if score <= 1:
        return False

    if score >= 100:
        return True
    # if is_substr(name_A.replace(' ', ''), name_B.replace(' ', '')) and len(name_A) > 10 and len(name_B) > 10:
    #     return True
    if (name_instance_A.first_name, name_instance_B.first_name) not in nickname_set and (name_instance_A.first_name, name_instance_B.first_name) not in nickname_initials_set:
        if not is_substr(name_instance_A.initials, name_instance_B.initials):
            return False
    else:
        if not is_substr(name_instance_A.initials[1:], name_instance_B.initials[1:]):
            return False

    # Chris Ding and Cui Ding
    if len(name_instance_A.first_name) > 1 and len(name_instance_B.first_name) > 1:
        if name_instance_A.first_name[0] == name_instance_B.first_name[0]:
            if (name_instance_A.first_name, name_instance_B.first_name) not in nickname_set:
                if (name_instance_A.first_name.find(name_instance_B.first_name) < 0 and name_instance_A.first_name.find(name_instance_B.first_name) < 0) \
                        or (name_instance_A.middle_name == '' and name_instance_B.middle_name == ''):
                    if not name_instance_A.bad_name_flag and not name_instance_B.bad_name_flag:
                        first_name_1 = name_instance_A.first_name.lower()
                        first_name_2 = name_instance_B.first_name.lower()
                        if name_instance_A.middle_name == name_instance_B.first_name or name_instance_B.middle_name == name_instance_A.first_name:
                            pass
                        elif name_instance_A.is_asian or name_instance_B.is_asian:
                            if SequenceMatcher(None, name_instance_A.first_name[1:], name_instance_B.first_name[1:]).ratio() < 0.93:
                                return False
                        else:
                            ldis = SequenceMatcher(None, name_instance_A.first_name[1:], name_instance_B.first_name[1:]).ratio()
                            if ldis < 0.93 and\
                                    (ldis < 0.80 or soundex(first_name_1) != soundex(first_name_2)):
                                return False
                    else:
                        if SequenceMatcher(None, name_instance_A.first_name[1:], name_instance_B.first_name[1:]).ratio() < 0.5:
                            return False

    # Michael Ia Jordan and Michael Ib jordan
    if len(name_instance_A.middle_name) > 1 and len(name_instance_B.middle_name) > 1:
        if name_instance_A.middle_name[0] == name_instance_B.middle_name[0]:
            if not is_substr(name_instance_A.middle_name.replace(' ', ''), name_instance_B.middle_name.replace(' ', '')):
                if SequenceMatcher(None, name_instance_A.middle_name[1:], name_instance_B.middle_name[1:]).ratio() <= 0.3:
                    return False

    # Michael Jordan and John Mohammed Jordan
    if name_instance_A.first_name[0] != name_instance_B.first_name[0] and (name_instance_A.first_name, name_instance_B.first_name) not in nickname_initials_set:
        if len(name_instance_B.middle_name) > 0:
            if name_instance_A.first_name[0] == name_instance_B.middle_name[0]:
                if len(name_instance_A.first_name) > 1 and len(name_instance_B.middle_name) > 1:
                    if my_string_match_score(name_instance_A.first_name, name_instance_B.middle_name, name_statistics) == 0:
                        return False
            else:
                if my_string_match_score(name_instance_A.name + ' ' + name_instance_A.middle_name,
                                         name_instance_B.first_name + ' ' + name_instance_B.first_name,
                                         name_statistics) == 0:
                    return False
        if len(name_instance_A.middle_name) > 0:
            if name_instance_B.first_name[0] == name_instance_A.middle_name[0]:
                if len(name_instance_B.first_name) > 1 and len(name_instance_A.middle_name) > 1:
                    if my_string_match_score(name_instance_A.middle_name, name_instance_B.first_name, name_statistics) == 0:
                        return False
            else:
                if my_string_match_score(name_instance_A.name + ' ' + name_instance_A.middle_name,
                                         name_instance_B.first_name + ' ' + name_instance_B.first_name,
                                         name_statistics) == 0:
                    return False

    if name_instance_A.last_name != name_instance_B.last_name:
        if SequenceMatcher(None, name_instance_A.last_name[1:], name_instance_B.last_name[1:]).ratio() <= 0.7:
            return False
        if SequenceMatcher(None, name_instance_A.last_name, name_instance_B.last_name).ratio() <= 0.7:
            return False

    return True


def __name_comparable(name_instance_A, name_instance_B, name_statistics, strict_mode=True):
    """Decide whether two name instances are comparable considering name reordering, not symmetric"""
    if single_name_comparable(name_instance_A, name_instance_B, name_statistics):
        return True

    name_A = '- '.join([name_instance_A.last_name, name_instance_A.middle_name, name_instance_A.first_name]).strip()
    new_name_instance_A = Name(name_A)
    new_name_instance_A.is_asian = name_instance_A.is_asian
    if single_name_comparable(new_name_instance_A, name_instance_B, name_statistics):
        return True

    name_A = '- '.join([name_instance_A.middle_name, name_instance_A.last_name, name_instance_A.first_name]).strip()
    new_name_instance_A = Name(name_A)
    new_name_instance_A.is_asian = name_instance_A.is_asian
    if single_name_comparable(new_name_instance_A, name_instance_B, name_statistics):
        return True

    name_A = '- '.join([name_instance_A.last_name, name_instance_A.first_name, name_instance_A.middle_name]).strip()
    new_name_instance_A = Name(name_A)
    new_name_instance_A.is_asian = name_instance_A.is_asian
    if single_name_comparable(new_name_instance_A, name_instance_B, name_statistics):
        return True

    name_A = '- '.join([name_instance_A.middle_name, name_instance_A.first_name, name_instance_A.last_name]).strip()
    new_name_instance_A = Name(name_A)
    new_name_instance_A.is_asian = name_instance_A.is_asian
    if strict_mode:
        if new_name_instance_A.name == name_instance_B.name:
            return True
    else:
        if single_name_comparable(new_name_instance_A, name_instance_B, name_statistics):
            return True

    name_A = '- '.join([name_instance_A.first_name, name_instance_A.last_name, name_instance_A.middle_name]).strip()
    new_name_instance_A = Name(name_A)
    new_name_instance_A.is_asian = name_instance_A.is_asian
    if single_name_comparable(new_name_instance_A, name_instance_B, name_statistics):
        return True

    return False


def name_comparable(name_instance_A, name_instance_B, name_statistics, strict_mode=True):
    """Decide whether two name instances are comparable considering name reordering, symmetric"""
    return __name_comparable(name_instance_A, name_instance_B, name_statistics, strict_mode) or __name_comparable(name_instance_B, name_instance_A, name_statistics, strict_mode)


def name_group_comparable(group, name_instance_dict, id_name_dict, name_statistics):
    """Decide whether two groups of name instances are comparable"""
    for author_A in group:
        for author_B in group:
            if author_A < author_B:
                if not name_comparable(name_instance_dict[id_name_dict[author_A][0]], name_instance_dict[id_name_dict[author_B][0]], name_statistics, False):
                    # print "\t\tConflicted name group: " + id_name_dict[author_A][0] + '\tv.s.\t' + id_name_dict[author_B][0]
                    return False
    return True


def name_group_comparable_with_tolerence(group, group1, group2, name_instance_dict, id_name_dict, name_statistics):
    """Decide whether two groups of name instances are comparable with certain tolerance"""
    total = len(group1) * len(group2) + 0.0
    disobey = 0
    for author_A in group1:
        for author_B in group2:
            if not name_comparable(name_instance_dict[id_name_dict[author_A][0]], name_instance_dict[id_name_dict[author_B][0]], name_statistics, False):
                disobey += 1
    if min(len(group1), len(group2)) >= 4:
        if disobey <= total * 0.2 or disobey <= min(len(group1), len(group2)) * 2:
            return True
        else:
            return False
    else:
        if disobey <= min(len(group1), len(group2)) / 2:
            return True
        else:
            return False


def compute_similarity_score(author_A, author_B, metapaths):
    """Compute similarity of two author ids based on metapaths"""
    if author_A not in normalized_feature_dict:
        feature_A = (metapaths.AP.getrow(author_A),
                     metapaths.APA.getrow(author_A),
                     metapaths.APV.getrow(author_A),
                     metapaths.APVPA.getrow(author_A),
                     metapaths.APK.getrow(author_A),
                     metapaths.AO.getrow(author_A),
                     metapaths.APAPA.getrow(author_A),
                     metapaths.APAPV.getrow(author_A),
                     metapaths.AY.getrow(author_A),
                     metapaths.APW.getrow(author_A))
        normalized_feature_A = (
            normalize(feature_A[0], norm='l2', axis=1),
            normalize(feature_A[1], norm='l2', axis=1),
            normalize(feature_A[2], norm='l2', axis=1),
            normalize(feature_A[3], norm='l2', axis=1),
            normalize(feature_A[4], norm='l2', axis=1),
            normalize(feature_A[5], norm='l2', axis=1),
            normalize(feature_A[6], norm='l2', axis=1))
            # normalize(feature_A[7], norm='l2', axis=1),
            # normalize(feature_A[8], norm='l2', axis=1),
            # normalize(feature_A[9], norm='l2', axis=1),
            # normalize(feature_A[10], norm='l2', axis=1)
        normalized_feature_dict[author_A] = normalized_feature_A
    else:
        normalized_feature_A = normalized_feature_dict[author_A]

    if author_B not in normalized_feature_dict:
        feature_B = (metapaths.AP.getrow(author_B),
                     metapaths.APA.getrow(author_B),
                     metapaths.APV.getrow(author_B),
                     metapaths.APVPA.getrow(author_B),
                     metapaths.APK.getrow(author_B),
                     metapaths.AO.getrow(author_B),
                     metapaths.APAPA.getrow(author_B),
                     metapaths.APAPV.getrow(author_B),
                     metapaths.AY.getrow(author_B),
                     metapaths.APW.getrow(author_A))
        normalized_feature_B = (
            normalize(feature_B[0], norm='l2', axis=1),
            normalize(feature_B[1], norm='l2', axis=1),
            normalize(feature_B[2], norm='l2', axis=1),
            normalize(feature_B[3], norm='l2', axis=1),
            normalize(feature_B[4], norm='l2', axis=1),
            normalize(feature_B[5], norm='l2', axis=1),
            normalize(feature_B[6], norm='l2', axis=1))
            # normalize(feature_B[7], norm='l2', axis=1),
            # normalize(feature_B[8], norm='l2', axis=1),
            # normalize(feature_B[9], norm='l2', axis=1),
            # normalize(feature_B[10], norm='l2', axis=1)
        normalized_feature_dict[author_B] = normalized_feature_B
    else:
        normalized_feature_B = normalized_feature_dict[author_B]

    similarity = (
        1000000 * normalized_feature_A[0].multiply(normalized_feature_B[0]).sum(),  # same paper
        100000 * normalized_feature_A[1].multiply(normalized_feature_B[1]).sum(),  # APA
        100000 * normalized_feature_A[2].multiply(normalized_feature_B[2]).sum(),  # AV
        1000 * normalized_feature_A[3].multiply(normalized_feature_B[3]).sum(),  # AVA
        # 1000 * normalized_feature_A[3].multiply(normalized_feature_B[6]).sum(),
        # 1000 * normalized_feature_A[6].multiply(normalized_feature_B[3]).sum(),
        100000 * normalized_feature_A[4].multiply(normalized_feature_B[4]).sum(),  # APK
        10000000 * normalized_feature_A[5].multiply(normalized_feature_B[5]).sum(),  # AO
        1000 * normalized_feature_A[6].multiply(normalized_feature_B[6]).sum(),  # APAPA
        # 1000 * normalized_feature_A[7].multiply(normalized_feature_B[7]).sum(),  # APKPA
        # 1000 * normalized_feature_A[8].multiply(normalized_feature_B[8]).sum(),  # APAPV
        # 1 * normalized_feature_A[9].multiply(normalized_feature_B[9]).sum(),  # AY
        # 1000 * normalized_feature_A[10].multiply(normalized_feature_B[10]).sum(),  # APW
        merge_threshold)

    return similarity


def merge_name_instances(name_instance_dict, id_name_dict, author_A, author_B):
    """Merge author_B's name instance into author_A's"""
    if id_name_dict[author_A][0] == id_name_dict[author_B][0]:
        return
    to_del = id_name_dict[author_B][0]
    for id in set(name_instance_dict[id_name_dict[author_B][0]].author_ids):
        name_instance_dict[id_name_dict[author_A][0]].add_author_id(id)
        id_name_dict[id][0] = id_name_dict[author_A][0]
    del name_instance_dict[to_del]


def local_clustering(similarity_dict, potential_duplicate_groups, author_paper_stat, name_instance_dict, id_name_dict, name_statistics, metapaths):
    """Detect duplicate pairs based on coauthor relationship between authors."""
    count = 0
    statistic = [0] * 14
    real_duplicate_groups = set()

    # Compute similarity between two name ids based on metapaths if their name are comparable
    for potential_duplicate_group in potential_duplicate_groups:
        if count % 10000 == 0:
            print("\tFinish computing similarities for " \
                + str(float(count)/len(potential_duplicate_groups)*100) \
                + "% (" + str(count) + "/" + str(len(potential_duplicate_groups)) \
                + ") possible duplicate groups.")
            print("\tStatistic about merges based on different features: " + str(statistic))
        count += 1

        author_A = potential_duplicate_group[0]
        author_B = potential_duplicate_group[1]
        name_A = id_name_dict[author_A][0]
        name_B = id_name_dict[author_B][0]
        if not name_comparable(name_instance_dict[name_A], name_instance_dict[name_B], name_statistics):
            continue

        if potential_duplicate_group not in similarity_dict:
            similarity = compute_similarity_score(author_A, author_B, metapaths)
            similarity_dict[potential_duplicate_group] = max(similarity)
            statistic[similarity.index(max(similarity))] += 1

    # Sort author pairs based on their similarity, then merge their name instances if necessary
    sorted_potential_duplicate_groups = sorted(list(similarity_dict.keys()), key=lambda x: -similarity_dict[x])
    for potential_duplicate_group in sorted_potential_duplicate_groups:
        if count % 10000 == 0:
            print("\tFinish merging " \
                + str(float(count)/len(potential_duplicate_groups)*100) \
                + "% (" + str(count) + "/" + str(len(potential_duplicate_groups)) \
                + ") possible duplicate groups.")
            print("\tStatistic about merges based on different features: " + str(statistic))
        count += 1

        author_A = potential_duplicate_group[0]
        author_B = potential_duplicate_group[1]

        name_A = id_name_dict[author_A][0]
        name_B = id_name_dict[author_B][0]

        if name_A == '' or name_B == '':
            continue

        if id_name_dict[author_A][0] not in name_instance_dict or id_name_dict[author_B][0] not in name_instance_dict:
            print("\t\t" + id_name_dict[author_A][0] + str(author_A))
            print("\t\t" + id_name_dict[author_B][0] + str(author_B))
            continue

        # if not name_comparable(name_instance_dict[name_A], name_instance_dict[name_B], name_statistics):
        #     continue

        name_instance_A = name_instance_dict[id_name_dict[author_A][0]]
        name_instance_B = name_instance_dict[id_name_dict[author_A][0]]

        # Merge two name instances
        if name_A != name_B:
            if len(name_A) <= 10 or len(name_B) <= 10:
                pass
            elif name_B.replace(' ', '').find(name_A.replace(' ', '')) >= 0 \
                    or name_A.replace(' ', '').find(name_B.replace(' ', '')) >= 0 \
                    or name_A.replace(' ', '') == name_B.replace(' ', '') \
                    or sorted(name_A.replace(' ', '')) == sorted(name_B.replace(' ', ''))\
                    or my_string_match_score(name_A, name_B, name_statistics, name_instance_A.is_asian or name_instance_B.is_asian) >= 10:
                if len(name_A.split()) > len(name_B.split()):
                    print("\t\tMerge two name instances: " + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)) + \
                          '   <--   ' + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)))
                    merge_name_instances(name_instance_dict, id_name_dict, author_A, author_B)
                elif len(name_A.split()) < len(name_B.split()):
                    print("\t\tMerge two name instances: " + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)) + \
                          '   <--   ' + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)))
                    merge_name_instances(name_instance_dict, id_name_dict, author_B, author_A)
                elif len(name_instance_dict[name_A].author_ids) > len(name_instance_dict[name_B].author_ids):
                    print("\t\tMerge two name instances: " + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)) + \
                          '   <--   ' + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)))
                    merge_name_instances(name_instance_dict, id_name_dict, author_A, author_B)

                elif len(name_instance_dict[name_A].author_ids) == len(name_instance_dict[name_B].author_ids):
                    score_A = 0
                    elements = name_A.split()
                    for i in range(len(elements) - 1):
                        if elements[i] + ' ' + elements[i + 1] in name_statistics:
                            score_A += name_statistics[elements[i] + ' ' + elements[i + 1]]
                    if len(elements) == 1:
                        score_A = 0
                    else:
                        score_A /= len(elements)
                    score_B = 0
                    elements = name_B.split()
                    for i in range(len(elements) - 1):
                        if elements[i] + ' ' + elements[i + 1] in name_statistics:
                            score_B += name_statistics[elements[i] + ' ' + elements[i + 1]]
                    if len(elements) == 1:
                        score_B = 0
                    else:
                        score_B /= len(elements)
                    if score_A > score_B:
                        print("\t\tMerge two name instances: " + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)) + \
                              '   <--   ' + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)))
                        merge_name_instances(name_instance_dict, id_name_dict, author_A, author_B)
                    elif score_A == score_B:
                        if len(name_B) >= len(name_A):
                            print("\t\tMerge two name instances: " + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)) + \
                                  '   <--   ' + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)))
                            merge_name_instances(name_instance_dict, id_name_dict, author_A, author_B)
                        else:
                            print("\t\tMerge two name instances: " + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)) + \
                                  '   <--   ' + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)))
                            merge_name_instances(name_instance_dict, id_name_dict, author_B, author_A)
                    else:
                        print("\t\tMerge two name instances: " + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)) + \
                              '   <--   ' + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)))
                        merge_name_instances(name_instance_dict, id_name_dict, author_B, author_A)
                else:
                    print("\t\tMerge two name instances: " + id_name_dict[author_B][1] + ': ' + str(len(name_instance_dict[name_B].author_ids)) + \
                          '   <--   ' + id_name_dict[author_A][1] + ': ' + str(len(name_instance_dict[name_A].author_ids)))
                    merge_name_instances(name_instance_dict, id_name_dict, author_B, author_A)

        real_duplicate_groups.add(potential_duplicate_group)

    return real_duplicate_groups


def merge_local_clusters(real_duplicate_groups, id_name_dict):
    """Merge local clusters.

    Parameters:
        real_duplicate_groups:
            A set of groups which contain duplicate author_ids separately.

    Returns:
        A dictionary of duplicate authors with key: author id and value:
        a list of duplicate author ids
    """
    id_group_dict = dict()
    print("\tMapping each author to his/her duplicate authors from duplicate groups.")
    for group in real_duplicate_groups:
        for author in group:
            id_group_dict.setdefault(author, list()).append(group)

    authors_duplicates_dict = dict()
    for (author_id, real_duplicate_groups) in id_group_dict.items():
        union_group = set()
        for group in real_duplicate_groups:
            union_group = union_group.union(group)
        authors_duplicates_dict[author_id] = union_group

    for author_id in id_name_dict.keys():
        authors_duplicates_dict.setdefault(author_id, set()).add(author_id)

    return authors_duplicates_dict


def find_conflict_name(authors_duplicates_dict, name_instance_dict, id_name_dict, name_statistics):
    """Find author ids whose duplicate author list contain conflicts in terms of their names"""
    conflict_ids = set()
    for (author_id, duplicate_group) in authors_duplicates_dict.items():
        if not name_group_comparable(duplicate_group, name_instance_dict, id_name_dict, name_statistics):
            conflict_ids.add(author_id)
    return conflict_ids


def find_closure(authors_duplicates_dict):
    """Find the closure of duplicate authors for each author id.
       Example : {1: [1, 2, 3, 4], 2: [2, 3, 4, 5]} -> {1: [2, 3, 4, 5], 2: [1, 3, 4, 5]}

    Parameters:
        authors_duplicates_dict
            A dictionary of duplicate authors with key: author id and value:
            a list of duplicate author ids
    """
    print("\tFinding close duplicate author set for each author id.")
    for author_id in authors_duplicates_dict.keys():
        authors_duplicates_dict[author_id].add(author_id)

    iteration = 0
    while True:
        print("\t\tIteration " + str(iteration))
        iteration += 1
        if iteration >= 100:
            break
        do_next_recursion = False
        for (author_id, duplicate_group) in authors_duplicates_dict.items():
            changed = False
            final_duplicate_group = set(duplicate_group)
            for _author_id in duplicate_group:
                if duplicate_group != authors_duplicates_dict[_author_id]:
                    changed = True
                    do_next_recursion = True
                    final_duplicate_group = final_duplicate_group.union(authors_duplicates_dict[_author_id])
            if changed:
                authors_duplicates_dict[author_id] = set(final_duplicate_group)
                for _author_id in duplicate_group:
                    authors_duplicates_dict[_author_id] = set(final_duplicate_group)
        if do_next_recursion is False:
            break

    for author_id in authors_duplicates_dict.keys():
        authors_duplicates_dict[author_id].remove(author_id)


def refine_result(authors_duplicates_dict, name_instance_dict, id_name_dict, name_statistics, similarity_dict, metapaths, remove_flag):
    """Filter obvious conflict names of duplicate authors for each author id."""
    for author_id in authors_duplicates_dict.keys():
        if author_id in authors_duplicates_dict[author_id]:
            authors_duplicates_dict[author_id].remove(author_id)

    if remove_flag:
        count = 0
        for author_id in authors_duplicates_dict.keys():
            for duplicate_author_id in set(authors_duplicates_dict[author_id]):
                if not name_comparable(name_instance_dict[id_name_dict[author_id][0]],
                                       name_instance_dict[id_name_dict[duplicate_author_id][0]],
                                       name_statistics,
                                       False):
                    authors_duplicates_dict[author_id].remove(duplicate_author_id)
                    if author_id in authors_duplicates_dict[duplicate_author_id]:
                        authors_duplicates_dict[duplicate_author_id].remove(author_id)
                    count += 1
        print("\tRemoving " + str(count) + " author_ids from name comparison.")

    conflict_ids = find_conflict_name(authors_duplicates_dict, name_instance_dict, id_name_dict, name_statistics)
    print("\tFinding who are really duplicates among the conflict author_ids")
    subset_similarity_dict = {}
    count = 0
    new_group_set = set()
    for author_id in conflict_ids:
        count += 1
        if count % 100 == 0:
            print("\tAdding pairwise similarities of " \
                + str(float(count)/len(conflict_ids)*100) \
                + "% (" + str(count) + "/" + str(len(conflict_ids)) \
                + ") conflict groups.")
        pool = authors_duplicates_dict[author_id]
        pool.add(author_id)
        for id in pool:
            new_group_set.add((id,))
        for candi1 in pool:
            for candi2 in pool:
                if candi1 != candi2:
                    if tuple(sorted((candi1, candi2))) not in similarity_dict:
                        similarity_dict[tuple(sorted((candi1, candi2)))] = max(compute_similarity_score(candi1, candi2, metapaths))
                    subset_similarity_dict[tuple(sorted((candi1, candi2)))] = similarity_dict[tuple(sorted((candi1, candi2)))]

    print("\tSorting conflicted author pairs according to similarity scores.")
    sorted_author_pairs = sorted(list(subset_similarity_dict.keys()), key=lambda candi: -subset_similarity_dict[candi])

    bad_pairs = list()
    for author_pair in sorted_author_pairs:
        author1 = author_pair[0]
        author2 = author_pair[1]
        group1 = tuple()
        for group in new_group_set:
            if author1 in group:
                group1 = group
            if author2 in group:
                group2 = group
        if group1 == group2:
            continue
        new_group = set(group1 + group2)
        if not name_group_comparable(new_group, name_instance_dict, id_name_dict, name_statistics):
            bad_pairs.append(author_pair)
            continue
        else:
            new_group = tuple(sorted(new_group))
        if group1 in new_group_set:
            new_group_set.remove(group1)
        if group2 in new_group_set:
            new_group_set.remove(group2)
        new_group_set.add(new_group)

    count = 0
    for author_pair in bad_pairs:
        count += 1
        if count % 1000 == 0:
            print("\tFinish merging " \
                + str(float(count)/len(bad_pairs)*100) \
                + "% (" + str(count) + "/" + str(len(bad_pairs)) \
                + ") conflict groups with tolerance.")
        author1 = author_pair[0]
        author2 = author_pair[1]
        group1 = tuple()
        for group in new_group_set:
            if author1 in group:
                group1 = group
            if author2 in group:
                group2 = group
        if group1 == group2:
            continue
        new_group = set(group1 + group2)
        if not name_group_comparable_with_tolerence(new_group, group1, group2, name_instance_dict, id_name_dict, name_statistics):
            continue
        else:
            new_group = tuple(sorted(new_group))
        if group1 in new_group_set:
            new_group_set.remove(group1)
        if group2 in new_group_set:
            new_group_set.remove(group2)
        new_group_set.add(new_group)

    for author_id in conflict_ids:
        new_group = authors_duplicates_dict[author_id]
        for group in new_group_set:
            if author_id in group:
                new_group = group
        for id in authors_duplicates_dict[author_id]:
            if id not in new_group and author_id in authors_duplicates_dict[id]:
                authors_duplicates_dict[id].remove(author_id)
        authors_duplicates_dict[author_id] = set(new_group)

    for author_id in authors_duplicates_dict.keys():
        if author_id in authors_duplicates_dict[author_id]:
            authors_duplicates_dict[author_id].remove(author_id)


def final_filter(author_paper_stat, name_statistics, authors_duplicates_dict, name_instance_dict, id_name_dict, similarity_dict, metapaths):
    """Filter obvious not confident names of duplicate authors for each author id."""
    count = 0
    for author_id in authors_duplicates_dict.keys():
        for duplicate_author_id in set(authors_duplicates_dict[author_id]):
            if not name_comparable(name_instance_dict[id_name_dict[author_id][0]],
                                   name_instance_dict[id_name_dict[duplicate_author_id][0]],
                                   name_statistics,
                                   False):
                authors_duplicates_dict[author_id].remove(duplicate_author_id)
                if author_id in authors_duplicates_dict[duplicate_author_id]:
                    authors_duplicates_dict[duplicate_author_id].remove(author_id)
                count += 1
    print("\tRemoving " + str(count) + " author_ids from name comparison.")

    for (author_id, candi_ids) in authors_duplicates_dict.items():
        if id_name_dict[author_id][0] not in name_instance_dict:
            continue
        for id in name_instance_dict[id_name_dict[author_id][0]].author_ids:
            if id in author_paper_stat and author_paper_stat[id] >= 1:
                authors_duplicates_dict[author_id] = authors_duplicates_dict[author_id].union(authors_duplicates_dict[id])
    for (author_id, candi_ids) in authors_duplicates_dict.items():
        for id in candi_ids:
            if id in author_paper_stat and author_paper_stat[id] >= 1 and id_name_dict[id][0] in name_instance_dict:
                authors_duplicates_dict[author_id] = authors_duplicates_dict[author_id].union(name_instance_dict[id_name_dict[id][0]].author_ids)
    for (author_id, candi_ids) in authors_duplicates_dict.items():
        if id_name_dict[author_id][0] not in name_instance_dict:
            continue
        for id in name_instance_dict[id_name_dict[author_id][0]].author_ids:
            if id in author_paper_stat and author_paper_stat[id] >= 1:
                authors_duplicates_dict[author_id] = authors_duplicates_dict[author_id].union(authors_duplicates_dict[id])
    for (author_id, candi_ids) in authors_duplicates_dict.items():
        for id in candi_ids:
            if id in author_paper_stat and author_paper_stat[id] >= 1 and id_name_dict[id][0] in name_instance_dict:
                authors_duplicates_dict[author_id] = authors_duplicates_dict[author_id].union(name_instance_dict[id_name_dict[id][0]].author_ids)
    for (author_id, candi_ids) in authors_duplicates_dict.items():
        if id_name_dict[author_id][0] not in name_instance_dict:
            continue
        for id in name_instance_dict[id_name_dict[author_id][0]].author_ids:
            if id in author_paper_stat and author_paper_stat[id] >= 1:
                authors_duplicates_dict[author_id] = authors_duplicates_dict[author_id].union(authors_duplicates_dict[id])
    for (author_id, candi_ids) in authors_duplicates_dict.items():
        for id in candi_ids:
            if id in author_paper_stat and author_paper_stat[id] >= 1 and id_name_dict[id][0] in name_instance_dict:
                authors_duplicates_dict[author_id] = authors_duplicates_dict[author_id].union(name_instance_dict[id_name_dict[id][0]].author_ids)
    count = 0
    for author_id in authors_duplicates_dict.keys():
        if len(authors_duplicates_dict[author_id]) == 1:
            name_A = id_name_dict[author_id][0]
            elements_A = name_A.split(' ')
            #remove  A Dgh EF and Abc EF pairs
            to_remove_set = set()
            for id in authors_duplicates_dict[author_id]:
                # if similarity_dict[tuple(sorted((id, author_id)))] > merge_threshold:
                #     continue
                name_B = id_name_dict[id][0]
                elements_B = name_B.split(' ')
                if ''.join(elements_A) == ''.join(elements_B):
                    continue
                if len(elements_A) > 2 and len(elements_A[0]) == 1 and len(elements_A[1]) > 1:
                    if len(elements_B[0]) > 1 and len(elements_B) == 2 and elements_A[0][0] == elements_B[0][0] and elements_A[1][0] != elements_B[0][0]:
                        to_remove_set.add(id)
                        count += 1
                        print('\t\tRemoving ' + name_B + ' from duplicates_set of ' + name_A)
                elif len(elements_B) > 2 and len(elements_B[0]) == 1 and len(elements_B[1]) > 1:
                    if len(elements_A[0]) > 1 and len(elements_A) == 2 and elements_B[0][0] == elements_A[0][0] and elements_B[1][0] != elements_A[0][0]:
                        to_remove_set.add(id)
                        count += 1
                        print('\t\tRemoving ' + name_B + ' from duplicates_set of ' + name_A)
            for id in to_remove_set:
                authors_duplicates_dict[author_id].remove(id)
        if len(authors_duplicates_dict[author_id]) <= 2:
            if author_id not in id_name_dict or id_name_dict[author_id][0] not in name_instance_dict:
                continue
            name_A = id_name_dict[author_id][0]
            elements_A = name_A.split(' ')
            #remove  A Dgh EF and Abc EF pairs
            to_remove_set = set()
            flag = 0
            for id in authors_duplicates_dict[author_id]:
                # if similarity_dict[tuple(sorted((id, author_id)))] > merge_threshold:
                #     continue
                name_B = id_name_dict[id][0]
                elements_B = name_B.split(' ')
                if max(len(elements_A), len(elements_B)) >= 3 and min(len(elements_A), len(elements_B)) == 2:
                    if tuple(sorted((id, author_id))) not in similarity_dict:
                        similarity_dict[tuple(sorted((id, author_id)))] = max(compute_similarity_score(id, author_id, metapaths))
                    if similarity_dict[tuple(sorted((id, author_id)))] <= merge_threshold:
                        flag += 1
                        stat1 = 0
                        if name_statistics[elements_A[-1]] <= 20:
                            continue
                        for element_A in elements_A:
                            if element_A in elements_B:
                                stat1 += 1
                            else:
                                if element_A in ' '.join(elements_B[:-1]):
                                    stat1 += 0.25
                        stat2 = 0
                        for element_B in elements_B:
                            if element_B in elements_A:
                                stat2 += 1
                            else:
                                if element_B in ' '.join(elements_A[:-1]):
                                    stat2 += 0.25
                        if max(stat1, stat2) <= 1.25:
                            to_remove_set.add(id)
                            count += 1
                            # print min(stat1, stat2)
                            print('\t\tRemoving ' + name_B + ' from duplicates_set of ' + name_A)
            if flag == len(authors_duplicates_dict[author_id]):
                for id in to_remove_set:
                    authors_duplicates_dict[author_id].remove(id)

    print("\tFinish removing " + str(float(count)) \
        + " unconfident names.")

    for author_id in authors_duplicates_dict.keys():
        if id_name_dict[author_id][1] == '':
            authors_duplicates_dict[author_id] = set()
    for author_id in authors_duplicates_dict.keys():
        if author_id in authors_duplicates_dict[author_id]:
            authors_duplicates_dict[author_id].remove(author_id)
        for id in set(authors_duplicates_dict[author_id]):
            if id not in author_paper_stat or author_paper_stat[id] == 0:
                authors_duplicates_dict[author_id].remove(id)
        if author_id not in author_paper_stat or author_paper_stat[author_id] == 0:
            authors_duplicates_dict[author_id] = set()
