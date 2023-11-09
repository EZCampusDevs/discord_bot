/*
 * Copyright (C) 2022-2023 EZCampus 
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

pipeline { 
    agent any  

        stages { 

            stage('Build Env File') {

                steps {

                    withCredentials([string(credentialsId: 'DISCORD_BOT_TOKEN', variable: 'DISCORD_TOKEN')]) {

                        writeFile file: './.env', text: """
BOT_TOKEN="${DISCORD_TOKEN}" 
"""
                        }
                }
            }

            stage('Build Docker Image') { 

                steps { 

                    sshPublisher(
                            failOnError: true,
                            publishers: [
                            sshPublisherDesc(
                                configName: '2GB_Glassfish_VPS',
                                transfers: [
                                sshTransfer(cleanRemote: true,
                                    excludes: '',
                                    execCommand: '''
                                    cd ~/pipeline_discord_bot
                                    ''',
                                    execTimeout: 120000,
                                    flatten: false,
                                    makeEmptyDirs: true, 
                                    noDefaultExcludes: false,
                                    patternSeparator: '[, ]+',
                                    remoteDirectory: 'pipeline_discord_bot',
                                    remoteDirectorySDF: false, 
                                    removePrefix: '', 
                                    sourceFiles: 'Dockerfile, requirements.txt, .env, entrypoint.sh, ezcampus/**')
                                ], 
                            usePromotionTimestamp: false,
                            useWorkspaceInPromotion: false,
                            verbose: false)
                                ])
                }
            }
        }

    post {

        always {

            discordSend(
                    description: currentBuild.result, 
                    enableArtifactsList: false, 
                    footer: '', 
                    image: '', 
                    link: '', 
                    result: currentBuild.result, 
                    scmWebUrl: '', 
                    thumbnail: '', 
                    title: env.JOB_BASE_NAME, 
                    webhookURL: "${DISCORD_WEBHOOK_1}"
                    )
        }
    }
}